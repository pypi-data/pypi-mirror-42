import itertools
import json
import logging
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Callable, Iterator, List, Optional, Sequence

import jsondiff

from r2c.lib.analyzer import Analyzer
from r2c.lib.constants import S3_ANALYSIS_BUCKET_NAME, SPECIAL_ANALYZERS
from r2c.lib.infrastructure import LocalDirInfra
from r2c.lib.manifest import AnalyzerManifest
from r2c.lib.registry import RegistryData
from r2c.lib.util import analyzer_name_from_dir, sort_two_levels
from r2c.lib.versioned_analyzer import VersionedAnalyzer

TEST_VECTOR_FOLDER = "examples"  # folder with tests
INTEGRATION_TEST_DIR_PREFIX = "/tmp/analysis-integration-"
LOCAL_RUN_TMP_FOLDER = "/tmp/local-analysis/"
CONTAINER_MEMORY_LIMIT = "2G"
UNITTEST_CMD = "/analyzer/unittest.sh"
UNITTEST_LOCATION = "src/unittest.sh"

logger = logging.getLogger(__name__)


class WorkdirNotEmptyError(Exception):
    """
        Thrown when a user-specified workdir is not an empty directory
        and the override flag is not provided
    """

    pass


def clone_repo(url, hash, target_path):
    logger.info(f"cloning for integration tests: {url} into {target_path}")
    subprocess.check_call(["git", "clone", "--quiet", url, target_path])
    subprocess.check_call(["git", "checkout", hash, "--quiet"], cwd=target_path)


def validator_for_test(test_filename: str, test_case_js):
    def validator(analyzer_output_path):
        output = json.load(open(analyzer_output_path))

        # we only want to sort two levels--the dicts and their keys. We don't
        # want to recurse and sort into the "extra" key that may be present
        diff = jsondiff.diff(
            sort_two_levels(test_case_js["expected"]),
            sort_two_levels(output["results"]),
        )
        if len(diff) > 0:
            logger.error(
                f"\n❌ test vector failed, actual output did not match expected for: {test_filename}, check {analyzer_output_path} and see below for diff:\n\n{diff}\n\n"
            )
            return False
        else:
            logger.error(f"\n✅ test vector passed: {test_filename}")
            return True

    return validator


def integration_test(analyzer_directory, workdir, env_args_dict, registry_data):
    test_vectors_path = os.path.join(analyzer_directory, TEST_VECTOR_FOLDER)
    with open(os.path.join(analyzer_directory, "analyzer.json"), "r") as f:
        manifest = AnalyzerManifest.from_json_str(f.read())

    analyzer_name = analyzer_name_from_dir(analyzer_directory)
    test_vectors: Sequence[str] = []
    if os.path.isdir(test_vectors_path):
        test_vectors = [f for f in os.listdir(test_vectors_path) if f.endswith(".json")]
    if len(test_vectors) > 0:
        logger.info(
            f"Found {len(test_vectors)} integration test vectors in {test_vectors_path}"
        )
    else:
        logger.warning(
            f"⚠️ No integration test vectors in examples directory: {test_vectors_path}"
        )

    results = {}
    test_times = {}
    for test_filename in test_vectors:
        logger.info(f"Starting test: {test_filename}")
        test_path = os.path.join(test_vectors_path, test_filename)
        with open(test_path) as test_content:
            try:
                js = json.load(test_content)
            except json.decoder.JSONDecodeError as ex:
                logger.error(f"invalid json in file: {test_path}: {str(ex)}")
                sys.exit(1)
            test_target = js["target"]
            test_target_hash = js["target_hash"]
            with tempfile.TemporaryDirectory(
                prefix=INTEGRATION_TEST_DIR_PREFIX
            ) as tempdir:
                clone_repo(test_target, test_target_hash, tempdir)
                validator = validator_for_test(
                    test_filename=test_filename, test_case_js=js
                )
                start_time = time.time()
                test_result = run_analyzer_on_local_code(
                    registry_data,
                    manifest=manifest,
                    workdir=workdir,
                    code_dir=tempdir,
                    wait=False,
                    no_preserve_workdir=True,
                    env_args_dict=env_args_dict,
                    report=False,
                    validator=validator,
                )
                results[test_path] = test_result
                test_times[test_path] = time.time() - start_time

    results_str = ""
    for test_path, result in results.items():
        status = "✅ passed" if result else "❌ failed"
        time_str = time.strftime("%H:%M:%S", time.gmtime(test_times[test_path]))
        results_str += f"\n\t{status}: {test_path} (time: {time_str})"
    # print to stdout
    print(results_str)
    num_passing = len([r for r in results.values() if r == True])
    print("##############################################")
    print(f"summary: {num_passing}/{len(results)} passed")
    if len(results) != num_passing:
        logger.error("integration test suite failed")
        sys.exit(-1)


def run_docker_unittest(
    analyzer_directory, analyzer_name, docker_image, verbose, env_args_dict
):
    env_args = list(
        itertools.chain.from_iterable(
            [["-e", f"{k}={v}"] for (k, v) in env_args_dict.items()]
        )
    )
    path = os.path.join(analyzer_directory, UNITTEST_LOCATION)
    if verbose:
        logger.info(f"Running unittest by executing {path}")
    if not os.path.exists(path):
        logger.warn(f"no unit tests for analyzer: {analyzer_name}")
        return 0
    docker_cmd = (
        ["docker", "run", "--rm"] + env_args + [f"{docker_image}", f"{UNITTEST_CMD}"]
    )
    if not verbose:
        docker_cmd.append(">/dev/null")
    if verbose:
        logger.error(f"running with {' '.join(docker_cmd)}")
    status = subprocess.call(docker_cmd)
    return status


def build_docker(docker_image, analyzer, version, env_args_dict, verbose):
    extra_build_args = [f"--build-arg {k}={v}" for (k, v) in env_args_dict.items()]
    build_cmd = f"docker build -t {docker_image} {analyzer} " + " ".join(
        extra_build_args
    )
    if verbose:
        build_cmd += " 1>&2"
    else:
        build_cmd += " >/dev/null"
    logger.debug(f"building with build command: {build_cmd}")
    status = subprocess.call(build_cmd, shell=True)
    return status


def docker_image(analyzer_name, version):
    return VersionedAnalyzer(analyzer_name, version).image_id


def run_analyzer_on_local_code(
    registry_data: RegistryData,
    manifest: AnalyzerManifest,
    workdir: Optional[str],
    code_dir: str,
    wait: bool,
    no_preserve_workdir: bool,
    report: bool,
    env_args_dict: dict,
    validator: Callable[[str], bool] = None,
):
    """
    Run an analyzer on a local folder, return the path to output json
    """
    infra = LocalDirInfra()
    infra.reset()
    pathlib.Path(LOCAL_RUN_TMP_FOLDER).mkdir(parents=True, exist_ok=True)

    # try adding the manifest of the current analyzer if it isn't already there
    if (
        not VersionedAnalyzer(manifest.analyzer_name, manifest.version)
        in registry_data.versioned_analyzers
    ):
        logger.info(
            "Analyzer manifest not present in registry. Adding it to the local copy of registry."
        )
        registry_data = registry_data.add_pending_manifest(manifest)
    else:
        logger.info("Analyzer manifest already present in registry")

    url_placeholder, commit_placeholder = get_local_git_origin_and_commit(code_dir)

    # get all cloner versions from registry so we can copy the passed in code directory in place
    # of output for all versions of cloner
    versions = [
        va for va in registry_data.versioned_analyzers if va.name in SPECIAL_ANALYZERS
    ]
    logger.info(
        f'"Uploading" (moving) code directory as the output of all cloners. Cloner versions: {versions}'
    )

    # No good way to provide an undefined-like as an argument to a func with a default arg
    if workdir is not None and os.path.exists(os.path.abspath(workdir)):
        abs_workdir = os.path.abspath(workdir)
        logger.info(f"CLI-specified workdir: {abs_workdir}")

        if len(os.listdir(abs_workdir)) > 0:
            if not no_preserve_workdir:
                logger.error(
                    "CLI-specified workdir is not empty! This directory must be empty or you must pass the `--no-preserve-workdir` option."
                )
                raise WorkdirNotEmptyError(abs_workdir)
            else:
                logger.warning(
                    "CLI-specified workdir is not empty, but override flag used!"
                )
                logger.warning(
                    "RUNNING ANALYZERS MAY MODIFY OR CLEAR WORKDIR CONTENTS WITHOUT WARNING!"
                )
                logger.warning("THIS IS YOUR LAST CHANCE TO BAIL OUT!")

        analyzer = Analyzer(
            infra, registry_data, localrun=True, workdir=abs_workdir, timeout=0
        )
    else:
        logger.info("Using default workdir")
        analyzer = Analyzer(infra, registry_data, localrun=True, timeout=0)

    for va in versions:
        with tempfile.TemporaryDirectory(prefix=LOCAL_RUN_TMP_FOLDER) as mount_folder:
            os.mkdir(os.path.join(mount_folder, "output"))

            if not os.path.exists(code_dir):
                raise Exception("that code directory doesn't exist")
            shutil.copytree(
                code_dir,
                os.path.join(mount_folder, "output", "fs"),
                symlinks=True,
                ignore_dangling_symlinks=True,
            )

            # "upload" output using our LocalDir infra (actually just a copy)
            cloner_image = docker_image(va.name, va.version)
            analyzer.upload_output(
                cloner_image, url_placeholder, commit_placeholder, mount_folder
            )

    start_ts = time.time()
    results = analyzer.full_analyze_request(
        url_placeholder,
        commit_placeholder,
        docker_image(manifest.analyzer_name, manifest.version),
        False,
        wait_for_start=wait,
        memory_limit=CONTAINER_MEMORY_LIMIT,
        env_args_dict=env_args_dict,
    )
    analyzer_time = time.time() - start_ts

    if validator:
        with tempfile.NamedTemporaryFile() as tempf:
            infra.get_file(
                S3_ANALYSIS_BUCKET_NAME, key=results["s3_key"], name=tempf.name
            )
            if validator:
                return validator(tempf.name)
    return None


def get_local_git_origin_and_commit(dir):
    try:
        repo = (
            subprocess.check_output(
                ["git", "config", "--get", "remote.origin.url"], cwd=dir
            )
            .strip()
            .decode("utf-8")
        )
        commit = (
            subprocess.check_output(
                ["git", "show", '--format="%H"', "--no-patch"], cwd=dir
            )
            .strip()
            .decode("utf-8")
        )
        return repo, commit.replace('"', "")
    except subprocess.CalledProcessError as ex:
        logger.error(f"failed to determine source git repo or commit for {dir}")
        return "[LOCAL_CODE]", "[LOCAL_CODE]"

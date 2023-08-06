#!/usr/bin/env python3
import json
import logging
import os
import pathlib
import shutil
import subprocess
import tarfile
import traceback
from datetime import datetime
from typing import Optional

import docker
import git
import jsonschema

from r2c.lib import schemas
from r2c.lib.constants import (
    S3_ANALYSIS_BUCKET_NAME,
    S3_ANALYSIS_LOG_BUCKET_NAME,
    S3_CODE_BUCKET_NAME,
    SPECIAL_ANALYZERS,
)
from r2c.lib.infrastructure import Infrastructure
from r2c.lib.manifest import AnalyzerManifest, AnalyzerOutputType, AnalyzerType
from r2c.lib.registry import RegistryData
from r2c.lib.util import Timeout, cloned_key, url_to_repo_id
from r2c.lib.versioned_analyzer import VersionedAnalyzer

MEMORY_LIMIT = (
    "1536m"
)  # clean t2.small with unbuntu 18.04 has Mem:           1991          92        1514           0         385        1752


class AnalyzerNonZeroExitError(Exception):
    """
        Thrown when analyzer docker container exists with non-zero exit code
    """

    def __init__(self, status_code, log):
        self._status_code = status_code
        self._log = log

    @property
    def log(self):
        return self._log

    @property
    def status_code(self):
        return self._status_code

    def __str__(self):
        return f"Docker Conatiner Finished with non-zero exit code: {self._status_code}"


class NotFoundInCodeBucket(Exception):
    """
        Thrown when cannot find file in code bucket
    """

    pass


class MalformedCodeBucketFile(Exception):
    """
        Thrown when file downloaded from code bucket fails to extract
        or is in an invalid state
    """

    pass


class AnalyzerImagePullFail(Exception):
    """
        Thrown when analyzer image fails to pull
    """

    pass


class UnsupportedAnalyzerType(Exception):
    """
        Thrown when unsupported analyzer type is encountered
    """

    pass


class InvalidAnalyzerOutput(Exception):
    """Thrown when the analyzer's output doesn't conform to its schema."""

    def __init__(self, inner: jsonschema.ValidationError):
        self.inner = inner


class Analyzer:
    def __init__(
        self,
        infra: Infrastructure,
        registry_data: RegistryData,
        localrun=False,
        timeout=1200,
        workdir="/tmp/analysis",
    ) -> None:
        self._infra = infra
        self._registry_data = registry_data
        self._logger = logging.getLogger("analyzer")
        self._docker_client = docker.from_env()
        self._timeout = timeout

        # TODO remove once cloner analyzer doesn't need to checkout
        self._localrun = localrun

        # Local run working dir. For analyzer use only.
        # THE CONTENTS OF THIS DIRECTORY MAY BE ERASED OR MODIFIED WITHOUT WARNING
        self._workdir = workdir
        self._registry_data = registry_data

    def reset_registry_data(self, registry_data: RegistryData):
        self._registry_data = registry_data

    def analysis_key(self, git_url: str, commit_hash: str, image_id: str) -> str:
        """
            Key analysis report was uploaded with

            Args:
                git_url: Url of repo analyzed
                commit_hash: hash analyzed
                image_id: full ECR id of docker container containing analyzer

            Returns:
                key of report in S3 bucket
        """
        manifest = self._get_manifest(image_id)

        output_type = manifest.output_type
        analyzer_type = manifest.analyzer_type

        repo_id = url_to_repo_id(git_url)

        if output_type == AnalyzerOutputType.json:
            extension = ".json"
        else:
            extension = ".tar.gz"

        if analyzer_type == AnalyzerType.git:
            key = f"{manifest.analyzer_name}/{manifest.version}/{repo_id}/output{extension}"
        elif analyzer_type == AnalyzerType.commit:
            key = f"{manifest.analyzer_name}/{manifest.version}/{repo_id}/{commit_hash}/output{extension}"
        else:
            raise UnsupportedAnalyzerType(analyzer_type)

        return key

    def resolve_commit_string(self, git_url: str, commit_string: str):
        """
            Return commit hash of checking out COMMIT_STRING in GIT_URL
            where commit_string can be tag, HEAD~1 etc.
        """
        if self._localrun:
            return commit_string

        # TODO do this without downloading repo
        repo_id = url_to_repo_id(git_url)
        repo_dir_name = os.path.join(self._workdir, "data", repo_id)
        self.get_code(git_url, repo_dir_name)

        repo = None
        try:
            repo = git.Repo(repo_dir_name)
        except Exception as e:
            raise MalformedCodeBucketFile(str(e))

        self._logger.info(f"Checking out {commit_string}")
        repo.git.checkout(commit_string)
        commit_hash = repo.head.object.hexsha
        self._logger.info(f"Has commit hash: {commit_hash}")
        self._logger.info(f"deleting {repo_dir_name}")
        shutil.rmtree(repo_dir_name)
        self._logger.info(f"Commit String {commit_string} has hash {commit_hash}")
        return commit_hash

    def full_analyze_request(
        self,
        git_url,
        commit_string,
        image_id,
        force,
        wait_for_start: bool = False,
        memory_limit: Optional[str] = None,
        env_args_dict: Optional[dict] = None,
    ):
        # Analyze head commit by default
        if not commit_string:
            commit_string = "HEAD"

        commit_hash = self.resolve_commit_string(git_url, commit_string)

        skipped = True

        execution_order = self._registry_data.sorted_deps(
            VersionedAnalyzer.from_image_id(image_id)
        )

        self._logger.info(
            f"All analyzers that will be run, in order: {execution_order}"
        )

        for dependency in execution_order:
            # TODO for now assume image_id format
            dependency_id = dependency.image_id
            output_s3_key = self.analysis_key(git_url, commit_hash, dependency_id)

            if (
                # TODO check freshness here
                self._infra.contains_file(S3_ANALYSIS_BUCKET_NAME, output_s3_key)
                and not force
            ):
                self._logger.info(
                    f"Analysis for {git_url} {commit_string} {dependency_id} already exists. Keeping old analysis report"
                )
            else:
                self._logger.info(
                    f"Running: {dependency.name}, {dependency.version}..."
                )
                mount_folder = self.analyze(
                    dependency_id,
                    git_url,
                    commit_hash,
                    wait_for_start=wait_for_start,
                    memory_limit=memory_limit,
                    env_args_dict=env_args_dict,
                )

                self._logger.info("Analyzer finished running.")
                try:
                    self._validate_output(
                        self._get_manifest(dependency_id), mount_folder
                    )
                except InvalidAnalyzerOutput:
                    # Invalid outputs should still be uploaded, but we want to
                    # count them as failing.
                    self.upload_output(
                        dependency_id, git_url, commit_hash, mount_folder
                    )
                    raise

                self.upload_output(dependency_id, git_url, commit_hash, mount_folder)

                self._logger.info(f"Deleting {mount_folder}")
                shutil.rmtree(mount_folder)
                skipped = False

        output_s3_key = self.analysis_key(git_url, commit_hash, image_id)
        return {"skipped": skipped, "commit_hash": commit_hash, "s3_key": output_s3_key}

    def _validate_output(self, manifest: AnalyzerManifest, mount_folder: str):
        """Validates the output, then migrates it to the latest schema.

        Note that if the analyzer's output is not JSON, this does nothing since
        we don't have a way to validate non-JSON outputs.

        Throws:
            InvalidAnalyzerOutput: If validation fails.

        """
        if manifest.output_type != AnalyzerOutputType.json:
            return

        path = os.path.join(mount_folder, "output", "output.json")
        with open(path) as f:
            output = json.load(f)

        manifest.output.validator(output).validate(output)
        try:
            manifest.output.validator(output).validate(output)
        except jsonschema.ValidationError as err:
            raise InvalidAnalyzerOutput(err) from err

    def upload_output(
        self, image_id: str, git_url: str, commit_hash: str, mount_folder: str
    ):
        """
            Upload analyzer results

            Args:
                image_id: docker container that was just run
                git_url: url of code analyzed
                commit_hash: hash of code analyzed
                mount_folder: volume mounted during analysis. Assumes output lives in
                mount_folder/output/output.json or mount_folder/output/fs
        """
        output_type = self._get_manifest(image_id).output_type

        output_s3_key = self.analysis_key(git_url, commit_hash, image_id)

        if output_type == AnalyzerOutputType.json:
            output_file = mount_folder + "/output/output.json"
        else:
            self._logger.info("Filesystem output type. Tarring output for uploading...")
            output_file = mount_folder + "/output/fs.tar.gz"
            with tarfile.open(output_file, "w:gz") as tar:
                tar.add(
                    mount_folder + "/output/fs", arcname=self.analyzer_name(image_id)
                )

        self._logger.info(
            f"Uploading {output_file} to {S3_ANALYSIS_BUCKET_NAME} with key {output_s3_key}"
        )
        self._infra.put_file(S3_ANALYSIS_BUCKET_NAME, output_file, output_s3_key)

    def get_code(self, git_url, dst):
        """
            Gets code for REPO_ID from S3, unzips, deletes zip file

            Raises:
                NotFoundInCodeBucket: if code for GIT_URL is not found in S3_CODE_BUCKET_NAME
                MalformedCodeBucketFile: if code found does not extract properly
        """
        repo_id = url_to_repo_id(git_url)
        repo_tar_name = os.path.join(self._workdir, f"{repo_id}.tar.gz")
        repo_s3_key = cloned_key(git_url)

        # Repo should not already exist. Probably invalid state. Best to just clean
        if pathlib.Path(repo_tar_name).exists():
            self._logger.info(f"{repo_tar_name} already exists. Deleting.")
            os.remove(repo_tar_name)
        if pathlib.Path(dst).exists():
            self._logger.info(f"{dst} already exists. Deleting")
            shutil.rmtree(dst)

        self._logger.info(
            f"Downloading {repo_s3_key} from {S3_CODE_BUCKET_NAME} to {repo_tar_name}"
        )
        if not self._infra.get_file(S3_CODE_BUCKET_NAME, repo_s3_key, repo_tar_name):
            self._logger.error(f"key {repo_s3_key} not found in {S3_CODE_BUCKET_NAME}")
            raise NotFoundInCodeBucket(
                f"key {repo_s3_key} not found in {S3_CODE_BUCKET_NAME}"
            )

        self._logger.info(f"Extracting to {dst}")

        try:
            with tarfile.open(repo_tar_name) as tar:
                tar.extractall(os.path.join(self._workdir, "data"))
                # This is only because the thing extracted from the tar is in a
                # directory named repo_id. Cloner should be changed to just have it
                # not have an extra directory level
                os.rename(os.path.join(self._workdir, "data", repo_id), dst)
        except Exception as e:
            raise MalformedCodeBucketFile(str(e))

        os.remove(repo_tar_name)

    @staticmethod
    def analyzer_name(image_id):
        """

        """
        return VersionedAnalyzer.from_image_id(image_id).name

    @staticmethod
    def analyzer_version(image_id):
        """
        """
        return VersionedAnalyzer.from_image_id(image_id).version

    def prepare_mount_volume(
        self, image_id: str, git_url: str, commit_hash: str
    ) -> str:
        """
            Prepares directory to be mounted to docker container IMAGE_ID to
            run analysis on GIT_URL on COMMIT_HASH. Raises exception when cannot
            prepare directory with necessary dependencies.

            Args:
                image_id: uniquely identifies docker image
                git_url: url of code
                commit_hash: hash to analyze code at

            Returns:
                mount_folder: path to root of volume prepared. For analyzer spec v3 this is
                the parent directory containing inputs/ and output/
        """
        now_ts = datetime.utcnow().isoformat().replace(":", "").replace("-", "")
        safe_image_id = image_id.split("/")[-1].replace(":", "__")
        mount_folder = os.path.join(
            self._workdir, f"{safe_image_id}__{commit_hash}__{now_ts}"
        )

        self._logger.info("Setting up volumes for analyzer container.")
        self._logger.info(f"Will mount: {mount_folder}")
        if pathlib.Path(mount_folder).exists():
            self._logger.debug(f"cleaning up old folder {mount_folder}")
            shutil.rmtree(mount_folder)

        input_dir = os.path.join(mount_folder, "inputs")
        output_dir = os.path.join(mount_folder, "output")
        pathlib.Path(input_dir).mkdir(parents=True, exist_ok=True)
        pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
        # TODO why should this only be done if we expect fs?
        pathlib.Path(os.path.join(mount_folder, "output", "fs")).mkdir(
            parents=True, exist_ok=True
        )

        dependencies = self._registry_data.get_direct_dependencies(
            VersionedAnalyzer.from_image_id(image_id)
        )

        if self.analyzer_name(image_id) in SPECIAL_ANALYZERS:
            with open(input_dir + "/cloner-input.json", "w") as argument_file:
                arguments = {"git_url": git_url, "commit_hash": commit_hash}
                json.dump(arguments, argument_file)
                success = True

        if self.analyzer_name(image_id) == "r2c/full-cloner":
            with open(input_dir + "/cloner-input.json", "w") as argument_file:
                arguments = {"git_url": git_url}
                json.dump(arguments, argument_file)
                success = True

        self._logger.info(f"Loading dependencies' outputs: {dependencies}")
        for dependency in dependencies:
            self._logger.info(f"Loading output of {dependency}")
            dependency_image_id = dependency.image_id
            self._logger.info(f"Has image_id: {dependency_image_id}")

            output_type = self._registry_data.manifest_for(dependency).output_type
            dependency_key = self.analysis_key(
                git_url, commit_hash, dependency_image_id
            )
            self._logger.info(
                f"Retrieving dependency output from s3 with key {dependency_key}"
            )

            # Ensure Target Location Exists
            pathlib.Path(os.path.join(input_dir, dependency.name)).mkdir(
                parents=True, exist_ok=True
            )

            if output_type == AnalyzerOutputType.json:
                success = self._infra.get_file(
                    S3_ANALYSIS_BUCKET_NAME,
                    dependency_key,
                    input_dir + "/" + dependency.name + ".json",
                )
            else:
                fs_input_tar = os.path.join(input_dir, "output.tar.gz")
                if self._infra.get_file(
                    S3_ANALYSIS_BUCKET_NAME, dependency_key, fs_input_tar
                ):
                    self._logger.info(f"Extracting filesystem dependency")
                    with tarfile.open(fs_input_tar) as tar:
                        tar.extractall(input_dir)
                    os.remove(fs_input_tar)
                    success = True
                else:
                    success = False

            if success:
                self._logger.info(f"Done setting up output of dependency {dependency}.")
            else:
                self._logger.error(
                    f"{dependency_key} could not be found. Failed to setup dependencies. Stopping Analysis."
                )
                raise Exception(
                    f"Could not prepare dependency: {dependency} does not exist."
                )

        return mount_folder

    def run_image_on_folder(
        self,
        image_id: str,
        mount_folder: str,
        wait_for_start: bool,
        memory_limit: Optional[str],
        env_args_dict: Optional[dict] = None,
    ):
        """
            Mount MOUNT_FOLDER as /analysis in docker container and run IMAGE_ID on it

            Args:
                image_id: uniquely identifies docker image
                mount_folder: path to directory we will mount as /analysis. In analyzer spec v3
                this is the directory that contains inputs/ and output. Assumes this directory is
                properly prepared
                wait_for_start: if true, change the run command so that it will wait infinitely instead of running the original Dockerfile CMD. Useful for debugging.
                memory_limit: memory limit for container, e.g. '2G'
            Raises:
                AnalyzerImagePullFail: if IMAGE_ID is not available and fails to pull
                TimeoutError: on timeout
                AnalyzerNonZeroExitError: when container exits with non-zero exit code
        """
        if not any(i for i in self._docker_client.images.list() if image_id in i.tags):
            self._logger.info(f"Image {image_id} not found. Pulling.")
            try:
                self._docker_client.images.pull(image_id)
            except Exception as e:
                raise AnalyzerImagePullFail(str(e))
        container = None

        # Prepare mount_folder to mount as volume to docker
        self._logger.info("Setup volume permissions")
        sudo_prefix = (
            [] if self._localrun else ["sudo"]
        )  # TODO REMOVE ONCE INFRA SUPPORTS RUNNING w/o SUDO TODO(brendongo)
        subprocess.call(
            sudo_prefix + ["chmod", "-R", "777", mount_folder]
        )  # wish we could do this in python but seems like a pain
        volumes = {}
        VOLUME_MOUNT_IN_DOCKER = "/analysis"
        volumes[mount_folder] = {"bind": VOLUME_MOUNT_IN_DOCKER, "mode": "rw"}

        # we can't use volume mounting with remote docker (for example, on
        # CircleCI), have to docker cp
        is_remote_docker = os.environ.get("DOCKER_HOST") is not None

        env_vars = (
            " ".join([f"-e {k}={v}" for k, v in env_args_dict.items()])
            if env_args_dict
            else ""
        )
        self._logger.info(
            f"""Running container {image_id} (memory limit: {memory_limit}): \n\t: debug with docker run {env_vars} --volume "{mount_folder}":{VOLUME_MOUNT_IN_DOCKER} {image_id}"""
        )
        try:
            with Timeout(self._timeout):
                if is_remote_docker:
                    self._logger.warning(
                        "Remote docker client, so volume mounts will not work--falling back to docker shell and cp'ing files"
                    )
                    if wait_for_start:
                        self._logger.error(
                            "Wait for start not supported with remote docker client"
                        )
                    container = self._docker_client.containers.create(
                        image_id,
                        volumes=None,
                        mem_limit=memory_limit if memory_limit else None,
                        environment=env_args_dict,
                    )
                    subprocess.check_output(
                        f'''docker cp "{mount_folder}/." {container.id}:"{VOLUME_MOUNT_IN_DOCKER}"''',
                        shell=True,
                    )
                    subprocess.check_output(f"docker start {container.id}", shell=True)
                else:
                    container = self._docker_client.containers.run(
                        image_id,
                        volumes=volumes,
                        detach=True,
                        command="tail -f /dev/null" if wait_for_start else None,
                        mem_limit=memory_limit if memory_limit else None,
                        environment=env_args_dict,
                    )

                if wait_for_start:
                    self._logger.info(
                        f"\n\nYour action required, container is ready: run\n\tdocker exec -i -t {container.id} /bin/bash"
                    )

                # Block until completion
                # We run with container detached so we can kill on timeout
                status = container.wait()

                # Retrieve status code and logs before removing container
                status_code = status.get("StatusCode")
                container_log = container.logs().decode("utf-8")
                print(container_log)
                # self._logger.info(f"Container output: {container_log}")

                if is_remote_docker:
                    self._logger.warning(
                        "Remote docker client, so volume mounts will not work--using cp to copying files out of container"
                    )
                    # c.f. https://docs.docker.com/engine/reference/commandline/cp/#extended-description for significance of /.
                    subprocess.check_output(
                        f'docker cp {container.id}:"{VOLUME_MOUNT_IN_DOCKER}/." "{mount_folder}"',
                        shell=True,
                    )

                container.remove()
                container = None

                # Change permissions of any new file added by container
                sudo_prefix = (
                    [] if self._localrun else ["sudo"]
                )  # TODO REMOVE ONCE INFRA SUPPORTS RUNNING w/o SUDO TODO(brendongo)
                subprocess.call(sudo_prefix + ["chmod", "-R", "777", mount_folder])

            if status_code != 0:
                self._logger.exception(
                    f"Docker Container Finished with non-zero exit code: {status_code}"
                )
                raise AnalyzerNonZeroExitError(status_code, container_log)

        except Exception as e:
            self._logger.exception(f"There was an error running {image_id}: {e}")

            if os.path.exists(mount_folder):
                self._logger.info(f"deleting {mount_folder}")
                # Change permissions of any new file added by container
                sudo_prefix = (
                    [] if self._localrun else ["sudo"]
                )  # TODO REMOVE ONCE INFRA SUPPORTS RUNNING w/o SUDO TODO(brendongo)
                subprocess.call(sudo_prefix + ["chmod", "-R", "777", mount_folder])
                shutil.rmtree(mount_folder, ignore_errors=True)

            if container:
                self._logger.info(f"killing container {container.id}")
                try:
                    # Kill and Remove Container as well as associated volumes
                    container.remove(v=True, force=True)
                    self._logger.info(f"successfully killed container {container.id}")
                except Exception:
                    self._logger.exception("error killing container")

            raise e

    def analyze(
        self,
        image_id: str,
        git_url: str,
        commit_hash: str,
        wait_for_start: bool,
        memory_limit: Optional[str],
        env_args_dict: Optional[dict] = None,
    ) -> str:
        """
            Run IMAGE_ID analyzer on GIT_URL @ COMMIT_HASH, retreiving dependencies from self._infra
            as necessary.

            Args:
                image_id: uniquely identifies docker image
                git_url: url of code
                commit_hash: hash of code to analyze at

            Returns:
                mount_folder: path to root of volume mounted. For analyzer spec v3 this is
                the parent directory containing inputs/ and output/
        """
        mount_folder = self.prepare_mount_volume(image_id, git_url, commit_hash)
        self.run_image_on_folder(
            image_id, mount_folder, wait_for_start, memory_limit, env_args_dict
        )
        return mount_folder

    def _get_manifest(self, image_id: str) -> AnalyzerManifest:
        """The manifest for this analyzer."""
        analyzer = VersionedAnalyzer.from_image_id(image_id)
        return self._registry_data.manifest_for(analyzer)

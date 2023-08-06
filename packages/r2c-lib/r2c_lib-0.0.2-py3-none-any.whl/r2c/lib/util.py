import base64
import json
import os
import signal
from collections import OrderedDict
from functools import cmp_to_key
from operator import itemgetter as i
from typing import NewType, Optional

import requests

from r2c.lib.constants import (
    ECR_URL,
    S3_ORG_REGISTRY_BUCKET_NAME,
    S3_PUBLIC_REGISTRY_BUCKET_NAME,
    S3_REGISTRY_FILENAME,
)
from r2c.lib.infrastructure import Infrastructure


class Timeout:
    """
        Helper class to wrap calls in a timeout

        Args:
            seconds (Int): number of seconds before timing out
            error_message (String): error message pass through when raising a TimeoutError. Default="Timeout"

        Return:
            Timeout object

        Raises:
            TimeoutError
    """

    def __init__(self, seconds=1, error_message="Timeout"):
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)


def sort_two_levels(iterable):
    # iterable is a list of dicts
    # [{ "C": 33, "A": 1, "B": 2 }, { "C": 33, "D": 1, "Z": 2 }] -> "
    # we need to create ordered dicts
    inner = [OrderedDict([(k, v) for k, v in sorted(x.items())]) for x in iterable]
    # should be valid for the sort to be on check_id and path, we're not
    # (currently) expecting duplicates of those
    return multikeysort(inner, ["check_id", "path"])


def multikeysort(items, columns):
    """
    Given an iterable of dicts, sort it by the columns (keys) specified in `columns` in order they appear.
    c.f. https://stackoverflow.com/questions/1143671/python-sorting-list-of-dictionaries-by-multiple-keys
    """

    # cmp was builtin in python2, have to add it for python3
    def cmp(a, b):
        return (a > b) - (a < b)

    comparers = [
        ((i(col[1:].strip()), -1) if col.startswith("-") else (i(col.strip()), 1))
        for col in columns
    ]

    def comparer(left, right):
        comparer_iter = (cmp(fn(left), fn(right)) * mult for fn, mult in comparers)
        return next((result for result in comparer_iter if result), 0)

    return sorted(items, key=cmp_to_key(comparer))


# TODO encapsualte encodings/key namings
def url_to_repo_id(git_url):
    """
        Returns repo_id used to identify GIT_URL in SQS and S3

        Reverse folder name for better cloud performance
        (otherwise prefixes are similar)
    """
    return base64.b64encode(git_url.encode("utf-8")).decode("utf-8")[::-1]


def repo_id_to_url(repo_id):
    """
        Inverse of url_to_repo_id. Returns GIT_URL from repo_id
    """
    return base64.b64decode(repo_id[::-1]).decode("utf-8")


def cloned_key(git_url):
    """
        Key code of GIT_URL was uploaded to S3 with
    """
    repo_id = url_to_repo_id(git_url)
    key = "{}.tar.gz".format(repo_id)
    return key


def analyzer_name_from_dir(analyzer_dir):
    """
        Get analyzer name from analyzer.json in a given analyzer directory
    """
    spec_path = os.path.join(analyzer_dir, "analyzer.json")
    if os.path.exists(spec_path):
        with open(spec_path) as f:
            try:
                spec = json.load(f)
                return spec.get("analyzer_name")
            except:
                raise
    return None

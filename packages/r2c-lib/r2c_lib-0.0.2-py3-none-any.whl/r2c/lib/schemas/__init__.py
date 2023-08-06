"""A package where we store all of our JSON schemas.

In general you don't need to look at the files within this directory, only the
methods that this exposes.
"""

import copy
import json
from importlib import resources
import logging
import sys
from typing import Optional

import jsonschema
from semantic_version import Version

logger = logging.getLogger(__name__)

SPEC_VERSION = Version("1.1.0")

_MANIFEST_SCHEMAS = {
    Version("1.0.0"): json.load(resources.open_text(__name__, "manifest.1.0.0.json")),
    Version("1.1.0"): json.load(resources.open_text(__name__, "manifest.1.1.0.json")),
}

# 1.0.0 and 1.1.0 both have the same output schema.

_ANALYZER_OUTPUT_SCHEMAS = {
    # 0.1.0 is a 'fake' version; some analyzers with spec version 1.0.0 output
    # something with a 0.1.0 spec_version that has some extra fields.
    Version("0.1.0"): json.load(
        resources.open_text(__name__, "analyzer_output.0.1.0.json")
    ),
    Version("1.0.0"): json.load(
        resources.open_text(__name__, "analyzer_output.1.0.0.json")
    ),
    Version("1.1.0"): json.load(
        resources.open_text(__name__, "analyzer_output.1.0.0.json")
    ),
}


def local_resolver(schema):
    """Constructs a RefResolver for the schema that resolves refs locally.

    Specifically, it defines a handler for the resource: URI schemes, which
    looks for schemas in this directory (r2c/schema), and defines handlers for
    all unsafe schemes that would normally be passed to urllib/requests that
    just throws a ValueError instead.

    This is necessary because jsonschema's default behavior allows arbitrary
    requests to external URIs.
    """

    def bad_uri_handler(uri):
        raise ValueError("URI {} uses an insecure scheme".format(uri))

    def resource_handler(uri):
        filename = uri[len("resource:") :]
        return json.load(resources.open_text(__name__, filename))

    handlers = {
        # We have to *explicitly* register handlers for unsafe schemes.
        "http": bad_uri_handler,
        "https": bad_uri_handler,
        "file": bad_uri_handler,
        "ftp": bad_uri_handler,
        "resource": resource_handler,
    }
    return jsonschema.RefResolver.from_schema(schema, handlers=handlers)


def analyzer_output_validator(
    output: dict,
    finding_schema: Optional[dict] = None,
    error_schema: Optional[dict] = None,
) -> jsonschema.Draft7Validator:
    """A validator for the output of the analyzer with the given manifest.

    Only works on the latest manifest version, so run migrations *before*
    calling this.

    In particular, this plugs in any declared schemas for the 'extra' fields on
    the results/errors into the standard analyzer output schema, then
    constructs a validator that validates against the new schema.
    """
    spec_version = Version(output.get("spec_version", "1.0.0"))
    schema = copy.deepcopy(_ANALYZER_OUTPUT_SCHEMAS[spec_version])
    if finding_schema is not None:
        schema["definitions"]["result"]["properties"]["extra"] = finding_schema
    if error_schema is not None:
        schema["definitions"]["error"]["properties"]["extra"] = error_schema
    return jsonschema.Draft7Validator(schema, resolver=local_resolver(schema))


def manifest_validator(manifest) -> Optional[jsonschema.Draft7Validator]:
    """Returns a validator for the given manifest, or None."""
    version = Version(manifest["spec_version"])
    if version > SPEC_VERSION:
        logging.warning(
            f"Input spec_version {version} is greater than any we know about; assuming latest known version {SPEC_VERSION} instead"
        )
        version = SPEC_VERSION
    schema = _MANIFEST_SCHEMAS.get(version)

    if schema is None:
        return None
    return jsonschema.Draft7Validator(schema, resolver=local_resolver(schema))

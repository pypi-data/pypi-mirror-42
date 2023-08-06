import json
from enum import Enum
from typing import Any, Dict, Optional, Union

import jsonschema
from mypy_extensions import TypedDict
from semantic_version import Version

from r2c.lib import manifest_migrations, schemas
from r2c.lib.versioned_analyzer import AnalyzerName


class AnalyzerType(Enum):
    constant = 1
    commit = 2
    git = 3

    @classmethod
    def from_name(cls, name):
        for t in AnalyzerType:
            if t.name == name:
                return t
        raise ValueError("{} is not a valid analyzer type".format(name))


class AnalyzerOutputType(Enum):
    json = 1
    filesystem = 2

    @classmethod
    def from_name(cls, name):
        for t in AnalyzerOutputType:
            if t.name == name:
                return t
        raise ValueError("{} is not a valid analyzer output type".format(name))


class _AnalyzerOutputJsonBase(TypedDict):
    type: str


class AnalyzerOutputJson(_AnalyzerOutputJsonBase, total=False):
    finding_extra_schema: Dict[str, Any]
    error_extra_schema: Dict[str, Any]


class _AnalyzerManifestJsonBase(TypedDict):
    analyzer_name: str
    version: str
    spec_version: str
    dependencies: Dict[str, str]
    type: str
    output: AnalyzerOutputJson
    deterministic: bool


class AnalyzerManifestJson(_AnalyzerManifestJsonBase, total=False):
    _original_spec_version: str


class AnalyzerOutput:
    def __init__(
        self,
        output_type: AnalyzerOutputType,
        finding_extra_schema: Optional[Dict[str, Any]],
        error_extra_schema: Optional[Dict[str, Any]],
    ):
        self._output_type = output_type
        self._finding_extra_schema = finding_extra_schema
        self._error_extra_schema = error_extra_schema

    @property
    def output_type(self) -> AnalyzerOutputType:
        return self._output_type

    @property
    def finding_extra_schema(self) -> Optional[Dict[str, Any]]:
        return self._finding_extra_schema

    @property
    def error_extra_schema(self) -> Optional[Dict[str, Any]]:
        return self._error_extra_schema

    @classmethod
    def from_json(cls, json_obj: AnalyzerOutputJson) -> "AnalyzerOutput":
        """Constructs from a JSON object. Does not validate the JSON."""
        return AnalyzerOutput(
            AnalyzerOutputType.from_name(json_obj["type"]),
            json_obj.get("finding_extra_schema", None),
            json_obj.get("error_extra_schema", None),
        )

    def to_json(self) -> AnalyzerOutputJson:
        json_obj: AnalyzerOutputJson = {"type": self._output_type.name}
        if self._finding_extra_schema:
            json_obj["finding_extra_schema"] = self._finding_extra_schema
        if self._error_extra_schema:
            json_obj["error_extra_schema"] = self._error_extra_schema
        return json_obj

    def validator(self, output: dict) -> jsonschema.Draft7Validator:
        """A validator that validates against the output schema, if any."""
        if self.output_type != AnalyzerOutputType.json:
            raise ValueError("Cannot get a validator for a non-JSON analyzer")
        return schemas.analyzer_output_validator(
            output,
            finding_schema=self.finding_extra_schema,
            error_schema=self.error_extra_schema,
        )


class AnalyzerManifest:
    def __init__(
        self,
        analyzer_name: AnalyzerName,
        version: Version,
        spec_version: str,
        dependencies: Dict[str, str],
        analyzer_type: AnalyzerType,
        output: AnalyzerOutput,
        deterministic: bool,
        original_json: Optional[Dict[str, Any]],
        original_spec_version: Optional[Version],
    ) -> None:
        self._analyzer_name = analyzer_name
        self._version = version
        self._spec_version = spec_version
        self._dependencies = dependencies
        self._analyzer_type = analyzer_type
        self._output = output
        self._deterministic = deterministic
        # The original JSON object. Useful for dumping out the original, in
        # case this got migrated. Should be `None` if this was synthesized
        # internally.
        self._original_json = original_json
        # The original spec version of this manifest.
        self._original_spec_version = original_spec_version or Version(spec_version)

    @property
    def analyzer_name(self) -> AnalyzerName:
        return self._analyzer_name

    @property
    def version(self) -> Version:
        return self._version

    @property
    def original_spec_version(self) -> Version:
        return self._original_spec_version

    @property
    def dependencies(self) -> Dict[str, str]:
        """
            The dependencies defined in this analyzer's manifest.
            These can be absolute versions or ranges and must be resolved.
        """
        return self._dependencies

    @property
    def analyzer_type(self) -> AnalyzerType:
        return self._analyzer_type

    @property
    def output(self) -> AnalyzerOutput:
        return self._output

    @property
    def output_type(self) -> AnalyzerOutputType:
        return self._output.output_type

    @property
    def deterministic(self) -> bool:
        return self._deterministic

    def to_json(self) -> AnalyzerManifestJson:
        json_obj: AnalyzerManifestJson = {
            "analyzer_name": str(self._analyzer_name),
            "version": str(self._version),
            "spec_version": self._spec_version,
            "dependencies": self._dependencies,
            "type": self._analyzer_type.name,
            "output": self._output.to_json(),
            "deterministic": self._deterministic,
        }
        if self.original_spec_version != schemas.SPEC_VERSION:
            json_obj["_original_spec_version"] = str(self._original_spec_version)
        return json_obj

    def to_original_json(self) -> Optional[Dict[str, Any]]:
        """The original JSON object this was constructed from.
        This is useful for displaying error messages to the user, since the
        output of to_json_obj() may not correspond to the user's input in cases
        of migration, default values, etc.
        Returns None if this was constructed directly.
        """
        return self._original_json

    @classmethod
    def from_json(cls, json_obj: Dict[str, Any]) -> "AnalyzerManifest":
        # The type of the json_obj argument is a bit of a hack, since in
        # r2c.lib.registry we cast an arbitrary dict to an AnalyzerManifestJson
        # before calling this.
        spec_version = json_obj.get("spec_version")
        if spec_version is None:
            raise MalformedManifestException(
                json_obj, "Must specify a spec_version field"
            )
        validator = schemas.manifest_validator(json_obj)
        if validator is None:
            raise MalformedManifestException(
                json_obj,
                "Could not find a schema for the given spec_version {}".format(
                    spec_version
                ),
            )
        try:
            validator.validate(json_obj)
        except jsonschema.ValidationError as err:
            raise MalformedManifestException(json_obj, err.message) from err

        original_json_obj = json_obj
        json_obj = manifest_migrations.migrate(json_obj)
        original_version = (
            Version(json_obj["_original_spec_version"])
            if json_obj.get("_original_spec_version")
            else Version(json_obj["spec_version"])
        )

        return cls(
            json_obj["analyzer_name"],
            Version(json_obj["version"]),
            json_obj["spec_version"],
            json_obj["dependencies"],
            AnalyzerType.from_name(json_obj["type"]),
            AnalyzerOutput.from_json(json_obj["output"]),
            json_obj["deterministic"],
            original_json_obj,
            original_version,
        )

    @classmethod
    def from_json_str(cls, json_str: str) -> "AnalyzerManifest":
        try:
            json_obj = json.loads(json_str)
        except:
            raise MalformedManifestException(json_str, "Can't parse json string")

        return AnalyzerManifest.from_json(json_obj)


class MalformedManifestException(Exception):
    def __init__(self, manifest: Union[str, Dict[str, Any]], message: str) -> None:
        self._manifest = manifest
        self._message = message

    def __str__(self) -> str:
        return "MalformedManifestException: could not parse {}. \n {}".format(
            self._manifest, self._message
        )


class InvalidManifestException(Exception):
    pass


class ManifestNotFoundException(Exception):
    pass

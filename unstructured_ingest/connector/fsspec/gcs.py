import typing as t
from dataclasses import dataclass
from pathlib import Path
from typing import Type

from unstructured_ingest.connector.fsspec.fsspec import (
    FsspecDestinationConnector,
    FsspecIngestDoc,
    FsspecSourceConnector,
    FsspecWriteConfig,
    SimpleFsspecConfig,
)
from unstructured_ingest.enhanced_dataclass import enhanced_field
from unstructured_ingest.error import SourceConnectionError
from unstructured_ingest.interfaces import AccessConfig
from unstructured_ingest.utils.dep_check import requires_dependencies
from unstructured_ingest.utils.string_and_date_utils import json_to_dict


@dataclass
class GcsAccessConfig(AccessConfig):
    token: t.Optional[str] = enhanced_field(
        default=None, sensitive=True, overload_name="service_account_key"
    )

    def __post_init__(self):
        ALLOWED_AUTH_VALUES = "google_default", "cache", "anon", "browser", "cloud"

        # Case: null value
        if not self.token:
            return
        # Case: one of auth constants
        if self.token in ALLOWED_AUTH_VALUES:
            return
        # Case: token as json
        if isinstance(json_to_dict(self.token), dict):
            self.token = json_to_dict(self.token)
            return
        # Case: path to token
        if Path(self.token).is_file():
            return

        raise ValueError("Invalid auth token value")


@dataclass
class GcsWriteConfig(FsspecWriteConfig):
    pass


@dataclass
class SimpleGcsConfig(SimpleFsspecConfig):
    access_config: GcsAccessConfig = None


@dataclass
class GcsIngestDoc(FsspecIngestDoc):
    connector_config: SimpleGcsConfig
    registry_name: str = "gcs"

    @SourceConnectionError.wrap
    @requires_dependencies(["gcsfs", "fsspec"], extras="gcs")
    def get_file(self):
        super().get_file()


@dataclass
class GcsSourceConnector(FsspecSourceConnector):
    connector_config: SimpleGcsConfig

    @requires_dependencies(["gcsfs", "fsspec"], extras="gcs")
    def initialize(self):
        super().initialize()

    def __post_init__(self):
        self.ingest_doc_cls: Type[GcsIngestDoc] = GcsIngestDoc


@dataclass
class GcsDestinationConnector(FsspecDestinationConnector):
    connector_config: SimpleGcsConfig
    write_config: GcsWriteConfig

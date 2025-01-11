import io
import json
import logging
import re
from itertools import chain
from urllib.parse import quote, urlparse

import validators
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from label_studio.io_storages.base_models import (
    ExportStorage,
    ExportStorageLink,
    ImportStorage,
    ImportStorageLink,
    ProjectStorageMixin,
)
from rest_framework.exceptions import ValidationError
from synology_api.filestation import FileStation

logger = logging.getLogger(__name__)

class SynologyException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class SynologyStorageMixin(models.Model):
    path = models.TextField(_('path'), null=True, blank=True, help_text='Path to Synology directory')
    url = models.TextField(_('url'), null=True, blank=True, help_text='URL to the Synology NAS')
    username = models.TextField(_('username'), null=True, blank=True, help_text='Username to the Synology NAS')
    password = models.TextField(_('password'), null=True, blank=True, help_text='Password to the Synology NAS')
    regex_filter = models.TextField(
        _('regex_filter'), null=True, blank=True, help_text='Cloud storage regex for filtering objects'
    )
    use_blob_urls = models.BooleanField(
        _('use_blob_urls'), default=False, help_text='Interpret objects as BLOBs and generate URLs'
    )

    @property
    def clean_url(self) -> str | None:
        parsed_url = urlparse(self.url)

        return f"{parsed_url.scheme}://{parsed_url.hostname}:{parsed_url.port}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__filestation: FileStation = None

    def get_filestation(self) -> FileStation:
        if self.__filestation is None:
            parsed_url = urlparse(self.clean_url)

            self.__filestation = FileStation(
                parsed_url.hostname,
                parsed_url.port,
                self.username,
                self.password,
                parsed_url.scheme == "https"
            )

        return self.__filestation
    
    def validate_connection_bool(self):
        try:
            # Throws an exception so we want to handle it.
            self.validate_connection()
            return True
        except:
            return False

    def validate_connection(self):
        if isinstance(validators.url(self.url), validators.ValidationError):
            raise ValidationError(f"URL is invalid.")
        
        parsed_url = urlparse(self.url)
        
        if isinstance(validators.hostname(parsed_url.hostname), validators.ValidationError):
            raise ValidationError(f"Host name is invalid")

        filestation = self.get_filestation()

        result = filestation.get_info()
        if not result["success"]:
            raise ValidationError(f"FileStation.get_info() returned '{result}'.")
        
        result = filestation.get_file_info(self.path)
        if not result["success"] or any("code" in f for f in result["data"]["files"]):
            raise ValidationError(f"FileStation.get_file_info() returned '{result}.")

class SynologyImportStorage(SynologyStorageMixin, ProjectStorageMixin, ImportStorage):
    def __get_files(self, path: str):
        filestation = self.get_filestation()

        result = filestation.get_file_list(path)
        if not result["success"] or "data" not in result:
            raise SynologyException(f"get_file_list returned '{result}'.")
        
        dir_files = chain(*[self.__get_files(f["path"]) for f in result["data"]["files"] if f["isdir"]])
        files = [f for f in result["data"]["files"] if not f["isdir"]]

        for file in chain(files, dir_files):
            yield file

    def can_resolve_url(self, url):
        filestation = self.get_filestation()
        result = filestation.get_file_info(url)

        return result["success"]
    
    def iterkeys(self):
        regex = re.compile(str(self.regex_filter)) if self.regex_filter else None

        # For better control of imported tasks, file reading has been changed to ascending order of filenames.
        # In other words, the task IDs are sorted by filename order.
        for file in sorted(self.__get_files(self.path), key=lambda x: x["name"]):
            key = file["name"]
            if regex and not regex.match(key):
                logger.debug(key + ' is skipped by regex filter')
                continue
            yield file["path"]

    def get_data(self, key):
        if self.use_blob_urls:
            data_key = settings.DATA_UNDEFINED_NAME
            return {data_key: f"{self.clean_url}{key}"}
        
        filestation = self.get_filestation()
        bytes: io.BytesIO = filestation.get_file(key, "serve")

        return json.loads(bytes.read())
    
    def resolve_uri(self, uri, task=None):
        parse_url = urlparse(uri)
        
        return f"{settings.HOSTNAME}/api/storages/synology/file?path={quote(parse_url.path)}&project={self.project.id}"
    
    def scan_and_create_links(self):
        return self._scan_and_create_links(SynologyImportStorageLink)
    
    def get_bytes(self, path: str) -> io.BytesIO:
        filestation = self.get_filestation()

        return filestation.get_file(path, "serve")

    class Meta:
        abstract = False

class SynologyExportStorage(SynologyStorageMixin, ExportStorage):
    pass

class SynologyImportStorageLink(ImportStorageLink):
    storage = models.ForeignKey(SynologyImportStorage, on_delete=models.CASCADE, related_name='links')

class SynologyExportStorageLink(ExportStorageLink):
    storage = models.ForeignKey(SynologyExportStorage, on_delete=models.CASCADE, related_name='links')
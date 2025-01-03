import io
import mimetypes

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from drf_yasg import openapi as openapi
from drf_yasg.utils import no_body, swagger_auto_schema
from label_studio.io_storages.api import (
    ExportStorageDetailAPI,
    ExportStorageFormLayoutAPI,
    ExportStorageListAPI,
    ExportStorageSyncAPI,
    ExportStorageValidateAPI,
    ImportStorageDetailAPI,
    ImportStorageFormLayoutAPI,
    ImportStorageListAPI,
    ImportStorageSyncAPI,
    ImportStorageValidateAPI,
)
# Using io_storages here is necessary to work around an issue with Django. Can't use label_studio.io_storages
from io_storages.synology.models import SynologyExportStorage, SynologyImportStorage
from label_studio.io_storages.synology.serializers import SynologyExportStorageSerializer, SynologyImportStorageSerializer
from rest_framework.views import APIView
from rest_framework.request import Request

from .openapi_schema import (
    _synology_export_storage_schema,
    _synology_export_storage_schema_with_id,
    _synology_import_storage_schema,
    _synology_import_storage_schema_with_id,
)

@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        tags=['Storage: Synology'],
        x_fern_sdk_group_name=['import_storage', 'synology'],
        x_fern_sdk_method_name='list',
        x_fern_audiences=['public'],
        operation_summary='Get all import storage',
        operation_description='Get a list of all Synology import storage connections.',
        manual_parameters=[
            openapi.Parameter(
                name='project',
                type=openapi.TYPE_INTEGER,
                in_=openapi.IN_QUERY,
                description='Project ID',
            ),
        ],
        request_body=no_body,
    ),
)
@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        tags=['Storage: Synology'],
        x_fern_sdk_group_name=['import_storage', 'synology'],
        x_fern_sdk_method_name='create',
        x_fern_audiences=['public'],
        operation_summary='Create import storage',
        operation_description='Create a new Synology import storage connection.',
        request_body=_synology_import_storage_schema,
    ),
)
class SynologyImportStorageListAPI(ImportStorageListAPI):
    queryset = SynologyImportStorage.objects.all()
    serializer_class = SynologyImportStorageSerializer

@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        tags=['Storage: Synology'],
        x_fern_sdk_group_name=['import_storage', 'synology'],
        x_fern_sdk_method_name='get',
        x_fern_audiences=['public'],
        operation_summary='Get import storage',
        operation_description='Get a specific Synology import storage connection.',
        request_body=no_body,
    ),
)
@method_decorator(
    name='patch',
    decorator=swagger_auto_schema(
        tags=['Storage: Synology'],
        x_fern_sdk_group_name=['import_storage', 'synology'],
        x_fern_sdk_method_name='update',
        x_fern_audiences=['public'],
        operation_summary='Update import storage',
        operation_description='Update a specific Synology import storage connection.',
        request_body=_synology_import_storage_schema,
    ),
)
@method_decorator(
    name='delete',
    decorator=swagger_auto_schema(
        tags=['Storage: Synology'],
        x_fern_sdk_group_name=['import_storage', 'synology'],
        x_fern_sdk_method_name='delete',
        x_fern_audiences=['public'],
        operation_summary='Delete import storage',
        operation_description='Delete a specific Synology import storage connection.',
        request_body=no_body,
    ),
)
class SynologyImportStorageDetailAPI(ImportStorageDetailAPI):
    queryset = SynologyImportStorage.objects.all()
    serializer_class = SynologyImportStorageSerializer

@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        tags=['Storage: Synology'],
        x_fern_sdk_group_name=['import_storage', 'synology'],
        x_fern_sdk_method_name='sync',
        x_fern_audiences=['public'],
        operation_summary='Sync import storage',
        operation_description='Sync tasks from a Synology import storage connection.',
        manual_parameters=[
            openapi.Parameter(
                name='id',
                type=openapi.TYPE_INTEGER,
                in_=openapi.IN_PATH,
                description='Storage ID',
            ),
        ],
        request_body=no_body,
    ),
)
class SynologyImportStorageSyncAPI(ImportStorageSyncAPI):
    serializer_class = SynologyImportStorageSerializer

@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        tags=['Storage: Synology'],
        x_fern_sdk_group_name=['export_storage', 'synology'],
        x_fern_sdk_method_name='sync',
        x_fern_audiences=['public'],
        operation_summary='Sync export storage',
        operation_description='Sync tasks from an Synology export storage connection.',
        request_body=no_body,
    ),
)
class SynologyExportStorageSyncAPI(ExportStorageSyncAPI):
    serializer_class = SynologyExportStorageSerializer

@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        tags=['Storage: Synology'],
        x_fern_sdk_group_name=['import_storage', 'synology'],
        x_fern_sdk_method_name='validate',
        x_fern_audiences=['public'],
        operation_summary='Validate import storage',
        operation_description='Validate a specific Synology import storage connection.',
        request_body=_synology_import_storage_schema_with_id,
        responses={200: openapi.Response(description='Validation successful')},
    ),
)
class SynologyImportStorageValidateAPI(ImportStorageValidateAPI):
    serializer_class = SynologyImportStorageSerializer

@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        tags=['Storage: Synology'],
        x_fern_sdk_group_name=['export_storage', 'synology'],
        x_fern_sdk_method_name='validate',
        x_fern_audiences=['public'],
        operation_summary='Validate export storage',
        operation_description='Validate a specific GCS export storage connection.',
        request_body=_synology_export_storage_schema_with_id,
        # expecting empty response
        responses={200: openapi.Response(description='OK')},
    ),
)
class SynologyExportStorageValidateAPI(ExportStorageValidateAPI):
    serializer_class = SynologyExportStorageSerializer


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        tags=['Storage: Synology'],
        x_fern_sdk_group_name=['export_storage', 'synology'],
        x_fern_sdk_method_name='list',
        x_fern_audiences=['public'],
        operation_summary='Get all export storage',
        operation_description='Get a list of all Synology export storage connections.',
        manual_parameters=[
            openapi.Parameter(
                name='project',
                type=openapi.TYPE_INTEGER,
                in_=openapi.IN_QUERY,
                description='Project ID',
            ),
        ],
        request_body=no_body,
    ),
)
@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        tags=['Storage: Synology'],
        x_fern_sdk_group_name=['export_storage', 'synology'],
        x_fern_sdk_method_name='create',
        x_fern_audiences=['public'],
        operation_summary='Create export storage',
        operation_description='Create a new Synology export storage connection to store annotations.',
        request_body=_synology_export_storage_schema,
    ),
)
class SynologyExportStorageListAPI(ExportStorageListAPI):
    queryset = SynologyExportStorage.objects.all()
    serializer_class = SynologyExportStorageSerializer

@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        tags=['Storage: Synology'],
        x_fern_sdk_group_name=['export_storage', 'synology'],
        x_fern_sdk_method_name='get',
        x_fern_audiences=['public'],
        operation_summary='Get export storage',
        operation_description='Get a specific Synology export storage connection.',
        request_body=no_body,
    ),
)
@method_decorator(
    name='patch',
    decorator=swagger_auto_schema(
        tags=['Storage: Synology'],
        x_fern_sdk_group_name=['export_storage', 'synology'],
        x_fern_sdk_method_name='update',
        x_fern_audiences=['public'],
        operation_summary='Update export storage',
        operation_description='Update a specific Synology export storage connection.',
        request_body=_synology_export_storage_schema,
    ),
)
@method_decorator(
    name='delete',
    decorator=swagger_auto_schema(
        tags=['Storage: Synology'],
        x_fern_sdk_group_name=['export_storage', 'synology'],
        x_fern_sdk_method_name='delete',
        x_fern_audiences=['public'],
        operation_summary='Delete export storage',
        operation_description='Delete a specific Synology export storage connection.',
        request_body=no_body,
    ),
)
class SynologyExportStorageDetailAPI(ExportStorageDetailAPI):
    queryset = SynologyExportStorage.objects.all()
    serializer_class = SynologyExportStorageSerializer

class SynologyImportStorageFormLayoutAPI(ImportStorageFormLayoutAPI):
    pass

class SynologyExportStorageFormLayoutAPI(ExportStorageFormLayoutAPI):
    pass

class SynologyImportGetFileAPI(APIView):
    serializer_class = SynologyImportStorageSerializer

    def get(self, request: Request):
        project_id = request.query_params["project"]

        path = request.query_params["path"]
        mimetype, _ = mimetypes.guess_type(path)

        # Get a list of storages which can satisfy this request.
        # There may be more than one, but should be at least one.
        storages = [
            s for s in SynologyImportStorage.objects.filter(project=project_id)
            if s.validate_connection_bool() and s.can_resolve_url(path)]

        if len(storages) == 0:
            raise ValueError("No storages returned.")

        # We don't need to be picky, all of these storages will get the job done.
        storage = storages[0]
        bytes: io.BytesIO = storage.get_bytes(path)

        return HttpResponse(bytes, content_type=mimetype)
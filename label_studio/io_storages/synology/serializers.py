import os

from label_studio.io_storages.serializers import ExportStorageSerializer, ImportStorageSerializer
# Using io_storages here is necessary to work around an issue with Django. Can't use label_studio.io_storages
from io_storages.synology.models import SynologyExportStorage, SynologyImportStorage
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class SynologyImportStorageSerializer(ImportStorageSerializer):
    type = serializers.ReadOnlyField(default=os.path.basename(os.path.dirname(__file__)))

    class Meta:
        model = SynologyImportStorage
        fields = '__all__'

    def validate(self, data):
        # Validate local file path
        data = super(SynologyImportStorageSerializer, self).validate(data)
        storage = SynologyImportStorage(**data)
        try:
            storage.validate_connection()
        except Exception as exc:
            raise ValidationError(exc)
        return data
    
class SynologyExportStorageSerializer(ExportStorageSerializer):
    type = serializers.ReadOnlyField(default=os.path.basename(os.path.dirname(__file__)))

    class Meta:
        model = SynologyExportStorage
        fields = '__all__'

    def validate(self, data):
        # Validate local file path
        data = super(SynologyExportStorageSerializer, self).validate(data)
        return data
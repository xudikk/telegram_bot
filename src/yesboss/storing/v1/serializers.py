import os
from rest_framework import serializers
from ..models import Files


class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True, source="file_path")

    def save(self):
        base, ext = os.path.splitext(self.validated_data.get('file_path', None).name)
        if ext in ['.png', '.jpg', '.jpeg']:
            self.validated_data['file_type'] = 1
        else:
            self.validated_data['file_type'] = 2

        fl = Files(**self.validated_data)
        fl.save()
        return fl

    class Meta:
        ref_name = "Files Store"
        model = Files
        fields = ('file', 'file_type')



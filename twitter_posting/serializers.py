from rest_framework import serializers
from .models import FileSchedularModel

class FileSchedularModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileSchedularModel
        fields = "__all__"
        error_messages ={"schedule_time": {"required": "Give yourself a username"}}

    def validate(self, data):
        if not( "schedule_time" in data):
            raise serializers.ValidationError("ENTER schedule_time")
        if data["file_field"]:
            value = data["file_field"].name
            if not(value.endswith(".mp4") or value.endswith(".mov") or value.endswith(".jpg") or value.endswith(".jpeg") or value.endswith(".png")):
                raise serializers.ValidationError('Valid formats are .mp4, .mov, .jpg, .jpeg, .png')

        return data

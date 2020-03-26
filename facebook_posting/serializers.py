from rest_framework import serializers
from .models import FBFileSchedularModel
from .forms import getFilename

class FBFileSchedularModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FBFileSchedularModel
        fields = "__all__"
        error_messages ={"schedule_time": {"required": "Give yourself a username"}}

    def validate(self, data):
        if not( "schedule_time" in data):
            raise serializers.ValidationError("ENTER schedule_time")
        if data["file_field"]:
            value = data["file_field"].name
            if value.endswith(".mov") or value.endswith(".MOV"):
                data["file_field"] = getFilename(value)+".mp4"
            if not(value.endswith(".mp4") or value.endswith(".mov") or value.endswith(".jpg") or value.endswith(".jpeg") or value.endswith(".png")
            or value.endswith(".JPG") or value.endswith(".JPEG") or value.endswith(".PNG") or value.endswith(".MP4")):
                raise serializers.ValidationError('Valid formats are .mp4, .mov, .jpg, .jpeg, .png')

        return data

from rest_framework import serializers


class RecordingChunkSerializer(serializers.Serializer):
    position = serializers.IntegerField()
    data = serializers.FileField()


class RecordingUpdateSerializer(serializers.Serializer):
    is_uploaded = serializers.BooleanField(required=False)
    name = serializers.CharField(required=False)


class DeviceSerializer(serializers.Serializer):
    token = serializers.CharField(min_length=128, max_length=128)

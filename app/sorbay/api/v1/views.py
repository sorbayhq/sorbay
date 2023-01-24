from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from sorbay.api.v1.serializers import (
    RecordingChunkSerializer,
    RecordingUpdateSerializer,
    DeviceSerializer
)
from users.models import Device
from recordings.models import Recording


class RecordingCreateView(APIView):
    """View that creates a new Recording (and checks if the corresponding bucket for uploads
     exists). This view gets called by the client right after the 'record' button is
     being clicked."""

    def post(self, request, *args, **kwargs):
        if not request.user.org.bucket_exists():
            request.user.org.create_bucket()
        recording = Recording.objects.create(
            org=request.user.org,
            uploaded_by=request.user,
        )
        return Response({
            "short_id": recording.short_id,
            "absolute_url": recording.get_absolute_url()
        }, status=status.HTTP_201_CREATED)


class RecordingUpdateView(APIView):
    """View to update an existing recording. Typically, this is used by the client to
    finalize an existing recording (by setting `is_uploaded` to `true`) and/or to update
    the name of the recording"""
    def patch(self, request, *args, **kwargs):
        try:
            # flake8 E128 continuation line under-indented for visual indent
            short_id = self.kwargs['short_id']
            recording = Recording.objects.get(short_id=short_id, org=request.user.org)
            serializer = RecordingUpdateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"detail": "invalid data", "err": serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)
            if is_uploaded := serializer.validated_data.get(
                    "is_uploaded",
                    None) is not None:
                recording.is_uploaded = is_uploaded
            if name := serializer.validated_data.get('name', None):
                recording.name = name[:128]
            recording.save(update_fields=["is_uploaded", "name"])
            Recording.objects.get(pk=recording.pk)
            return Response({
                "short_id": recording.short_id,
                "absolute_url": recording.get_absolute_url()
            }, status=status.HTTP_202_ACCEPTED)
        except Recording.DoesNotExist:
            return Response({
                "detail": "no such recording",
            }, status=status.HTTP_404_NOT_FOUND)


class RecordingChunkView(APIView):
    """View to upload a chunk of a recording. Accepts `.webm` files with H264 video codec,
    transcodes them and uploads them to S3.
    # todo: this should probably start some kind of task in the background, see
    # todo: `recordings.models.Recording.add_chunk` for further notes on that
    """
    def post(self, request, *args, **kwargs):
        recording = Recording.objects.get(
            short_id=self.kwargs['short_id'],
            org=request.user.org
        )
        serializer = RecordingChunkSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={"detail": "invalid data", "err": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        recording.add_chunk(
            position=serializer.validated_data['position'],
            chunk=serializer.validated_data['data']
        )
        return Response({"is": "ok"})


class DeviceKeyView(APIView):
    """View to exchange an API key for a device token. Used during
    the client authentication process.

    See `users.views.DeviveRegisterView` for more notes on the process."""
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            try:
                device = Device.objects.get(token=serializer.data['token'])
                # the exchange API key <-> device token can only happen once.
                # if the key is being returned by the view, set `is_key_exchanged`
                # to true so that no further exchanges can happen
                if device.is_key_exchanged:
                    return Response({"detail": "key has already been exchanged"},
                                    status=status.HTTP_403_FORBIDDEN)
                device.is_key_exchanged = True
                device.save(update_fields=['is_key_exchanged'])
            except Device.DoesNotExist:
                return Response({"detail": "device not found"},
                                status=status.HTTP_404_NOT_FOUND)
            return Response({
                "key": device.api_key,
                "user": {
                    "first_name": device.user.first_name,
                    "last_name": device.user.last_name,
                    "email": device.user.email,
                    "id": device.user.id
                }
            })
        return Response({"detail": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)

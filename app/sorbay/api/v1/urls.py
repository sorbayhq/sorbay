from django.urls import path

from sorbay.api.v1.views import (
    RecordingCreateView,
    RecordingUpdateView,
    RecordingChunkView,
    DeviceKeyView
)

app_name = "api-v1"
urlpatterns = [
    path("recordings/", RecordingCreateView.as_view()),
    path("recordings/<str:short_id>/", RecordingUpdateView.as_view()),
    path("recordings/chunk/<str:short_id>/", RecordingChunkView.as_view()),
    path("device/key/", DeviceKeyView.as_view())
]

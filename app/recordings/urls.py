from django.urls import path

from recordings.views import DashboardView, RecordingDetailView, RecordingPlayListView

app_name = "recordings"
urlpatterns = [
  path("", DashboardView.as_view(), name="dashboard"),
  path("<str:short_id>/", RecordingDetailView.as_view(), name="detail"),
  # flake8 E501 line too long (91 > 90 characters)
  path("<str:short_id>/playlist.m3u8", RecordingPlayListView.as_view(), name="playlist"),
]

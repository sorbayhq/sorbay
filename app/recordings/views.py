import decimal
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView, DetailView

from recordings.models import Recording, View as RecordingView


class RecordingPlayListView(View):
    """View that creates an m3u8 playlist/stream on the fly based
    on the metadata that's in a `recordings.models.Recording`'s `chunk`s."""
    content_type = "application/vnd.apple.mpegurl"
    http_method_names = ['get', 'options']

    def get(self, request, *args, **kwargs):
        recording = get_object_or_404(
            Recording,
            short_id=self.kwargs['short_id']
        )
        max_duration = max(
            [Decimal(chunk['duration']).to_integral_exact(rounding=decimal.ROUND_CEILING)
             for chunk in recording.chunks]
        )
        m3u8 = "#EXTM3U\n"
        m3u8 += "#EXT-X-VERSION:4\n"
        m3u8 += f"#EXT-X-TARGETDURATION:{max_duration}\n"
        m3u8 += "#EXT-X-MEDIA-SEQUENCE:0\n"
        m3u8 += "#EXT-X-PLAYLIST-TYPE:VOD\n"
        # todo: EXT-X-DISCONTINUITY seems to not be working on Safari. Leaving it out
        # renders the stream unusable on Firefox/Chrome. Leave this out for now
        m3u8 += "#EXT-X-DISCONTINUITY\n"
        for chunk in sorted(recording.chunks, key=lambda c: c['position']):
            m3u8 += "\n"
            # this sets the offset for the current chunk. This, however
            # on some browsers doesn't seem to work. Leave it out for now.
            # if chunk['position'] > 0:
            #     offset = str(sum([Decimal(c['duration']) for c in recording.chunks if
            #                       c['position'] < chunk['position']]))
            #     m3u8 += f"#EXT-X-START:TIME-OFFSET={offset},\n"
            m3u8 += f"#EXT-X-DISCONTINUITY-SEQUENCE:{chunk['position']}\n"
            m3u8 += f"#EXTINF:{chunk['duration']},\n"
            m3u8 += chunk['url']
        m3u8 += "\n#EXT-X-ENDLIST\n"
        return HttpResponse(m3u8, content_type=self.content_type)


class DashboardView(LoginRequiredMixin, TemplateView):
    """View displaying all the recordings a user has recorded."""
    template_name = "recordings/dashboard.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['recordings'] = Recording.objects.filter(
            is_uploaded=True,
            org=self.request.user.org
        ).order_by("-created_at")
        return data


class RecordingDetailView(DetailView):
    """View that represents the detail view of a video.

    Creates a `recordings.models.View` object and updates the `view_count` of a
    `recordings.models.Recording`."""
    model = Recording
    context_object_name = "recording"
    template_name = "recordings/detail.html"

    def get_object(self, queryset=None):
        recording = get_object_or_404(
            Recording,
            short_id=self.kwargs['short_id']
        )
        user = self.request.user if self.request.user.is_authenticated else None
        if user == recording.uploaded_by:
            return recording
        # if the user is not authenticated or the user viewing this is not actually the
        # user that has uploaded it, create a View to count the number of views
        RecordingView.objects.create(
            user=user,
            recording=recording
        )
        # optimize the view count by updating the view_count on the video model. That's
        # repetitive but is an optimization that's worth it as it reduces the workload
        # on the database significantly
        Recording.objects.filter(pk=recording.pk).update(view_count=F("view_count") + 1)
        return recording

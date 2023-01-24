import os
from decimal import Decimal
from io import BytesIO
from tempfile import NamedTemporaryFile

from django.conf import settings
from django.db import models
from django.urls import reverse
from shortuuid.django_fields import ShortUUIDField


class Recording(models.Model):
    """Model holding all the information on a recording.

    A recording typically belongs first and foremost to an organisation and not the user.
    If a user ever decides to leave the platform, the organisation should still have
    access to the recordings."""
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128)
    short_id = ShortUUIDField(length=8, unique=True)
    org = models.ForeignKey('organisations.Organisation', on_delete=models.CASCADE)
    chunks = models.JSONField(default=list)
    uploaded_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    is_uploaded = models.BooleanField(default=False)
    # the view_count is an optimization of View.objects.filter(recording=self).count()
    # to make it easier on the database. It is updated whenever a recording view occurs
    view_count = models.IntegerField(default=0)

    def get_absolute_url(self):
        """The URL to the recording detail page"""
        return settings.HOST + reverse("recordings:detail", kwargs={
            "short_id": self.short_id,
        })

    def add_chunk(self, position, chunk):
        """Adds a chunk to the recording, by:

        - transcoding the original chunk to H264/AAC
        - uploading it to S3
        - updating the recording metadata on the position/duration

        # todo: this whole process needs to be broken down into multiple parts,
        # todo: possibly be made async in some way (celery task). The
        # todo: function is currently transcoding + uploading, which is taxing on the
        # todo: CPU + needs some time. But: overengineering is the root of all evil,
        # todo: so we leave it like this for now.
        """
        # create temporary files for the chunk and the m3u8
        with NamedTemporaryFile("wb", delete=False) as chunk_file:
            chunk_file.write(chunk.file.read())
        with NamedTemporaryFile(delete=False) as m3u8_file:
            m3u8_path = m3u8_file.name
        # transcode the file. The codec should already be H264, so we only
        # need to transcode the codec to AAC
        os.system(
            f"ffmpeg -hide_banner -loglevel error "
            f"-i {chunk_file.name} -codec: copy -acodec aac "
            f"-start_number 0 -hls_time 10 -hls_list_size 0 "
            f"-f hls {m3u8_path}"
        )
        # get the duration of the chunk by parsing the m3u8
        with open(m3u8_path, "r") as m3u8_file:
            duration = None
            for line in m3u8_file.readlines():
                if line.startswith("#EXTINF:"):
                    duration = Decimal(line.split(':')[1].split(',')[0])
                    break
        chunk_name = f"chunk-{str(position)}.ts"
        # upload the transcoded chunk to s3
        self.org.s3.meta.client.upload_fileobj(
            Fileobj=BytesIO(open(m3u8_path + "0.ts", "rb").read()),
            Bucket=self.org.bucket,
            Key=f"public/{self.short_id}/{chunk_name}"
        )
        # add metadata so that we are later able to create a full m3u8 for the recording
        self.chunks.append({
            "position": position,
            "name": chunk_name,
            "url": f"{settings.S3_PUBLIC_ENDPOINT_URL}/{self.org.bucket}"
                   f"/public/{self.short_id}/{chunk_name}",
            "duration": str(duration)
        })
        self.save(update_fields=['chunks'])

        # clean up all the temporary files
        for file_name in (chunk_file.name, m3u8_file.name):
            if os.path.exists(file_name):
                os.remove(file_name)


class View(models.Model):
    """Model representing a view on a Recording.
    Can have a user associated with it."""
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True,
                             default=None)
    recording = models.ForeignKey('Recording', on_delete=models.CASCADE)

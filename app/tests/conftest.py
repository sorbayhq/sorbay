from tempfile import NamedTemporaryFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
import os
import pytest

from recordings.models import Recording
from users.models import User
from organisations.models import Organisation


@pytest.fixture
def org():
    organisation = Organisation.objects.create(name="testorg")
    organisation.create_bucket()
    return organisation


@pytest.fixture
def user(org):
    return User.objects.create_user(
        username="testuser",
        password="testpass",
        org=org
    )


@pytest.fixture
def recording(org, user):
    black_recording = Recording.objects.create(
        name="recording",
        org=org,
        uploaded_by=user,
        is_uploaded=True
    )
    with NamedTemporaryFile("rb", delete=False) as file:
        os.system(
            # creating a black screen one second video
            f"ffmpeg -f lavfi -i color=size=1280x720:rate=25:color=black "
            f"-f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 "
            f"-t 1 "
            f"{file.name}.webm 2> /dev/null"
        )
        with open(f"{file.name}.webm", "rb") as chunk_file:
            chunk_io = io.BytesIO(chunk_file.read())
            file_name = chunk_file.name
            file_size = os.stat(chunk_file.name).st_size
        chunk = InMemoryUploadedFile(
            file=chunk_io,
            field_name="ChunkField",
            name=file_name,
            content_type="webm",
            size=file_size,
            charset=None
        )
        black_recording.add_chunk(0, chunk)
    return black_recording

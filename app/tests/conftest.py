import pytest

from recordings.models import Recording
from users.models import User
from organisations.models import Organisation


@pytest.fixture
def org():
    return Organisation.objects.create(name="testorg")


@pytest.fixture
def user(org):
    return User.objects.create_user(
        username="testuser",
        password="testpass",
        org=org
    )


@pytest.fixture
def recording(org, user):
    return Recording.objects.create(
        name="recording",
        org=org,
        uploaded_by=user,
        is_uploaded=True
    )

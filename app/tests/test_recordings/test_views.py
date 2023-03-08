import pytest
import uuid
from django.urls import reverse


@pytest.mark.django_db
def test_dashboard_view(client, user):
    test_url = reverse("recordings:dashboard")
    authentication_url = f"/oidc/authenticate/?next={test_url}"

    response = client.get(test_url)
    assert response.status_code == 302
    assert response.headers["Location"] == authentication_url

    client.force_login(user)
    response = client.get(test_url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_detail_view(client, recording):
    # uuid of a recording that exists in the database
    true_uuid = recording.short_id
    # made up uuid of a non existent recording
    fake_uuid = str(uuid.uuid4())[:8]

    true_test_url = reverse("recordings:detail", kwargs={"short_id": true_uuid})
    fake_test_url = reverse("recordings:detail", kwargs={"short_id": fake_uuid})

    # no log-in is required
    response = client.get(true_test_url)
    assert response.status_code == 200

    response = client.get(fake_test_url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_playlist_view(client, recording):
    # uuid of a recording that exists in the database
    true_uuid = recording.short_id
    # made up uuid of a non existent recording
    fake_uuid = str(uuid.uuid4())[:8]

    true_test_url = reverse("recordings:playlist", kwargs={"short_id": true_uuid})
    fake_test_url = reverse("recordings:playlist", kwargs={"short_id": fake_uuid})

    # no log-in is required
    response = client.get(true_test_url)
    assert response.status_code == 200

    response = client.get(fake_test_url)
    assert response.status_code == 404

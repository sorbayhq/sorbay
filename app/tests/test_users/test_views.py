import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_settings_view(client, user):
    response = client.get(reverse("users:settings"))
    assert response.status_code == 302

    client.force_login(user)
    response = client.get(reverse("users:settings"))
    assert response.status_code == 200

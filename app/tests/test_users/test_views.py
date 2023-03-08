import pytest
import json
from django.urls import reverse


@pytest.mark.django_db
def test_settings_view(client, user):
    test_url = reverse("users:settings")
    authentication_url = f"/oidc/authenticate/?next={test_url}"

    response = client.get(test_url)
    assert response.status_code == 302
    assert response.headers["Location"] == authentication_url

    client.force_login(user)
    response = client.get(test_url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_device_register_view(client, user):
    data = {
        "token": "",
        "name": "",
        "application": "",
        "release": "",
    }
    payload = json.dumps(data)

    test_url = reverse("users:device-register", kwargs={"payload": payload})
    authentication_url = reverse("oidc_authentication_init")

    response = client.get(test_url)
    assert response.status_code == 302
    assert authentication_url in response.headers["Location"]

import pytest
import json
from django.urls import reverse


@pytest.mark.django_db
def test_settings_view(client, user):
    response = client.get(reverse("users:settings"))
    assert response.status_code == 302
    assert response.headers["Location"] == f"/oidc/authenticate/?next={reverse('users:settings')}"

    client.force_login(user)
    response = client.get(reverse("users:settings"))
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
    response = client.get(reverse("users:device-register", kwargs={"payload": payload}))
    assert response.status_code == 302
    assert reverse("oidc_authentication_init") in response.headers["Location"]

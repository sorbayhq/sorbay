import pytest
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

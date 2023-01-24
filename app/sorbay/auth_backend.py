from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User, Device

from django.conf import settings
from django.utils.http import urlencode

from organisations.models import Organisation


class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    """Custom OIDC authentication backend, meant to be used with Mozillas OIDC
    implementation for Django.
    """

    def create_user(self, claims):
        """Creates a user and (if required) an Organisation for the user"""
        # todo: implement organisation mapping here for users that bring their
        # own single sign on. This should be possible using client specific mappers
        # https://github.com/keycloak/keycloak-ui/issues/2511
        org = Organisation.objects.create()
        return User.objects.create_user(
            username=self.get_username(claims),
            email=claims.get("email"),
            org=org,
            first_name=claims.get("given_name"),
            last_name=claims.get("family_name")
        )

    def filter_users_by_claims(self, claims):
        """Return all users matching the username (in claims['sub'])"""
        return User.objects.filter(username=self.get_username(claims))

    def get_username(self, claims):
        """Get the username from the claim"""
        return claims.get('sub')

    def update_user(self, user, claims):
        """Update existing user with new claims, if necessary save, and return user"""
        user.email = claims.get("email")
        user.first_name = claims.get("given_name")
        user.last_name = claims.get('family_name')
        user.save()
        return user


class DeviceAPIAuthenticationBackend(BaseAuthentication):
    """Custom backend to authenticate users based on an API key that's configured
    for a device."""

    def authenticate(self, request):
        # flake8 T001 print found.
        # print("authing request", request.headers.get("X-API-Key", ""))
        # flake8 T001 print found.
        # print([d.api_key for d in Device.objects.all()])
        api_key = request.headers.get("X-API-Key", "")
        if not api_key:
            # flake8 T001 print found.
            # print("not key")
            return None
        if len(api_key) != 64:
            # flake8 T001 print found.
            # print("no good length")
            return AuthenticationFailed("Invalid API Key")
        try:
            device = Device.objects.get(api_key=api_key)
        except Device.DoesNotExist:
            raise AuthenticationFailed("No such device")
        # for whatever reason, this should return a tuple
        return (device.user, None)


def provider_logout(request):
    """Custom logout function that performs a logout on Django + Keycloak"""
    query = {
        'post_logout_redirect_uri': request.build_absolute_uri(
            settings.LOGOUT_REDIRECT_URL
        ),
        'client_id': settings.OIDC_RP_CLIENT_ID
    }
    returned_value = settings.OIDC_OP_LOGOUT_ENDPOINT + '?' + urlencode(query)
    return returned_value

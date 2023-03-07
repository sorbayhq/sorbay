"""
The intended use for this code is to set up Keycloak in the development environment. It is
meant to be run during the setup process and heavily relies on the environment to be set 
correctly.
"""
import os
import time
from django.conf import settings
from keycloak import KeycloakAdmin
from keycloak.exceptions import KeycloakConnectionError

is_setup_ready = False

while not is_setup_ready:
    try:
        keycloak_admin = KeycloakAdmin(
            server_url="http://keycloak:8080/",
            username=os.environ['KEYCLOAK_ADMIN'],
            password=os.environ['KEYCLOAK_ADMIN_PASSWORD'],
            realm_name="master",
            verify=True
        )
    except KeycloakConnectionError:
        print("waiting for the keycloak setup")
        time.sleep(3)
        continue
    is_setup_ready = True
keycloak_admin.create_realm(payload={
    "id": "dev",
    "realm": "dev",
    "displayName": "Dev",
    "enabled": True,
    "sslRequired": "external",
    "registrationAllowed": True,
    "registrationEmailAsUsername": True,
    "rememberMe": True,
    "verifyEmail": False,
    "loginWithEmailAllowed": True,
    "duplicateEmailsAllowed": False,
    "resetPasswordAllowed": True,
    "editUsernameAllowed": False,
    "bruteForceProtected": False,
    "defaultSignatureAlgorithm": "RS256",
    "loginTheme": "sorbay",
})
keycloak_admin.realm_name = "dev"
keycloak_admin.create_client(payload={
    "clientId": "auth",
    "name": "auth",
    "enabled": True,
    "clientAuthenticatorType": "client-secret",
    "secret": settings.OIDC_RP_CLIENT_SECRET,
    "redirectUris": [
        "",
        "http://0.0.0.0:8000/",
        "http://localhost:8000/",
        "http://0.0.0.0:8000/oidc/callback/",
        "http://localhost:8000/oidc/callback/"
    ],
    "attributes": {
        "post.logout.redirect.uris":
            "http://0.0.0.0:8000/##"
            "http://localhost:8000/"
    }
})

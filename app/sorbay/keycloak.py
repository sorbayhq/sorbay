import logging
from django.conf import settings
from keycloak import KeycloakAdmin

from users.models import User


class KeycloakError(Exception):
    pass


logger = logging.getLogger(__name__)


class KeycloakAPI:
    """API, giving direct access to the Keycloak server"""

    @property
    def keycloak_admin(self):
        keycloak_admin = KeycloakAdmin(
            server_url=settings.KEYCLOAK_URL,
            username=settings.KEYCLOAK_ADMIN_USER,
            password=settings.KEYCLOAK_ADMIN_PASSWORD,
            realm_name="master",
            verify=True
        )
        keycloak_admin.realm_name = settings.KEYCLOAK_REALM
        return keycloak_admin

    def create_user(self, email, first_name, last_name, role, verified_email, credentials,
                    org=None, ):
        """Creates a new user on Keycloak and in Django"""
        logger.info(f"Creating user {email}")
        id = self.keycloak_admin.create_user(
            {
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
                "enabled": True,
                "emailVerified": verified_email,
                "username": email,
                "credentials": credentials,
            }
        )
        u = User.objects.create_user(
            username=id,
            email=email,
            org=org,
            role=role,
            first_name=first_name,
            last_name=last_name
        )
        return u

    def change_password(self, user, new_password, temporary):
        self.keycloak_admin.set_user_password(
            password=new_password,
            temporary=temporary,
            user_id=user.keycloak_id
        )

    def change_email(self, user, email):
        self.keycloak_admin.update_user(
            user_id=user.keycloak_id,
            payload={"email": email}
        )

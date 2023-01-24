import secrets

with open("/mnt/code/.envs/.dev.example", "r") as in_file:
    with open("/mnt/code/.envs/.dev", "w") as out_file:
        data = in_file.read()
        for key in (
                "POSTGRES_PASSWORD",
                "MINIO_ROOT_PASSWORD",
                "SECRET_KEY",
                "KEYCLOAK_ADMIN_PASSWORD",
                "OIDC_RP_CLIENT_SECRET"
        ):
            data = data.replace(f"<CHANGE_{key}>", secrets.token_urlsafe(32))
        out_file.write(data)

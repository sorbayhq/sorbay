#!/bin/bash

set -o errexit
set -o pipefail

# in development, we set the S3 access and secret key to the minio root user
# ========= DON'T USE IN PRODUCTION =========
export S3_ACCESS_KEY="$MINIO_ROOT_USER"
export S3_SECRET_KEY="$MINIO_ROOT_PASSWORD"

# forward requests to port 8080 to the keycloak server running in its own container.
# this solves a lot of headaches when authenticating via oauth, because we
# don't have to solve the localhost(frontend) <-> keycloak(backend) mapping on
# ever side.
# ========= DON'T USE IN PRODUCTION =========
socat TCP-LISTEN:8080,fork TCP:keycloak:8080 &
exec "$@"

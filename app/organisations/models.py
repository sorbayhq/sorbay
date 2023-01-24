import json

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.db import models
from shortuuid.django_fields import ShortUUIDField


class Organisation(models.Model):
    """Model holding all the information on an Organisation.

    The organisation is the main hub for a user to hold actual configuration data. Every
    user has an organisation, even though he might never collaborate on the platform
    with other members."""
    name = models.CharField(max_length=48, null=True, default=None)
    short_id = ShortUUIDField(
        length=8, unique=True
    )
    bucket_id = ShortUUIDField(
        length=8, unique=True,
        alphabet=list("1234567890abcdefghijklmnopqrstuvwxyz")
    )

    @property
    def bucket(self):
        """The S3 bucket that belongs to the organisation"""
        return f"sorbay-{self.bucket_id}"

    @property
    def s3(self):
        """Convienence property to access the s3 api on behalf of the Organisation"""
        return boto3.resource(
            's3',
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY
        )

    def bucket_exists(self):
        """Checks if the bucket in `self.bucket` actually exists on s3"""
        try:
            self.s3.meta.client.head_bucket(Bucket=self.bucket)
            return True
        except ClientError:
            return False

    def create_bucket(self):
        """Creates the bucket in `self.bucket` and makes all content under /public/
        publicly accessible."""
        self.s3.meta.client.create_bucket(Bucket=self.bucket)
        self.s3.meta.client.put_bucket_policy(
            Bucket=self.bucket,
            Policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": ["s3:GetObject"],
                        "Resource": [f"arn:aws:s3:::{self.bucket}/public/*"]
                    }
                ]
            }))

    def create_presigned_upload_url(self, recording, filename):
        """Creates a presigned upload URL that can be sent down to clients."""
        data = self.s3.meta.client.generate_presigned_post(
            Bucket=self.bucket,
            Key='public/' + recording.short_id + "/" + filename,
        )
        if settings.S3_ENDPOINT_URL in data['url']:
            data['url'] = data['url'].replace(
                settings.S3_ENDPOINT_URL,
                settings.S3_PUBLIC_ENDPOINT_URL
            )
        return data

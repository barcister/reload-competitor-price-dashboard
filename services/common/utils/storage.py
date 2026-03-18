from datetime import datetime

import boto3

from services.common.utils.settings import settings


class SnapshotStorage:
    def __init__(self) -> None:
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint_url,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
        )

    def put_text(self, connector: str, payload: str) -> str:
        key = f"{connector}/{datetime.utcnow().isoformat()}.txt"
        self.client.put_object(Bucket=settings.s3_bucket, Key=key, Body=payload.encode("utf-8"))
        return f"s3://{settings.s3_bucket}/{key}"

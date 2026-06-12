import os
import getpass
import pandas as pd
import s3fs
DEFAULT_ENDPOINT = "https://minio.terrafoxai.com"

# Module-level state tracking
_user = None
_password = None
_endpoint = DEFAULT_ENDPOINT


def connect(user=None, password=None, endpoint=None):
    """Initializes and caches connection credentials for the session."""
    global _user, _password, _endpoint

    # 1. Resolve Endpoint
    _endpoint = endpoint or os.environ.get("MINIO_ENDPOINT") or DEFAULT_ENDPOINT
    
    # 2. Resolve Username
    _user = user or os.environ.get("MINIO_USER") or os.environ.get("AWS_ACCESS_KEY_ID")
    
    # 3. Resolve Password
    _password = password or os.environ.get("MINIO_PASSWORD") or os.environ.get("AWS_SECRET_ACCESS_KEY")

    # 4. Fallback to interactive terminal prompts if still missing
    if not _user or not _password:
        print("🔐 Data Lake credentials not found in environment settings.")
        if not _user:
            _user = input("Enter MinIO Username: ")
        if not _password:
            # getpass masks the password characters in terminal/Colab outputs
            _password = getpass.getpass("Enter MinIO Password: ")

    # 5. Export variables to environment context for s3fs backend systems
    os.environ["AWS_ACCESS_KEY_ID"] = _user
    os.environ["AWS_SECRET_ACCESS_KEY"] = _password

    print("🚀 Terrafox Data Lake Connected!")


def read_csv(bucket, key, **kwargs):
    """Wrapper that reads a CSV straight from the S3 backend into Pandas."""
    global _user, _password, _endpoint
    
    if not _user or not _password:
        connect()

    path = f"s3://{bucket}/{key}"

    return pd.read_csv(
    path,
    storage_options={
        "key": _user,
        "secret": _password,
        "client_kwargs": {
            "endpoint_url": _endpoint
        },
        "config_kwargs": {
            "signature_version": "s3v4"
        }
    },
    **kwargs
)


def ls(path=""):
    """
    List files and directories in the data lake.

    Examples:
        dl.ls()
        dl.ls("Data")
        dl.ls("Data/Clinical Data")
    """
    global _user, _password, _endpoint

    if not _user or not _password:
        connect()

    fs = s3fs.S3FileSystem(
        key=_user,
        secret=_password,
        client_kwargs={
            "endpoint_url": _endpoint
        },
        config_kwargs={
            "signature_version": "s3v4"
        }
    )

    bucket_path = "bigdata"

    if path:
        bucket_path += f"/{path.strip('/')}"

    return fs.ls(bucket_path)
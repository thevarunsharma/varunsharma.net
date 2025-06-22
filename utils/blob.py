import logging
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient
from app import generate_webpage


def upload_webpage_to_blob(storage_account_name: str, container_name: str, blob_name: str) -> None:
    logging.info("Generating HTML content for upload")

    # Generate HTML content
    html = generate_webpage()

    # Use Managed Identity
    credential = DefaultAzureCredential()
    blob_url = f"https://{storage_account_name}.blob.core.windows.net"

    # Upload
    blob_client = BlobClient(
        account_url=blob_url,
        container_name=container_name,
        blob_name=blob_name,
        credential=credential
    )
    blob_client.upload_blob(html, overwrite=True)
    logging.info(f"Uploaded {blob_name} to container {container_name}")

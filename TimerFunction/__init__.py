import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential

from utils.blob import upload_webpage_to_blob


STORAGE_ACCOUNT_NAME = "varunsharmanet"
CONTAINER_NAME = "www"


def main(mytimer: func.TimerRequest = None, req: func.HttpRequest = None) -> func.HttpResponse | None:
    """
    Timer trigger function to upload a webpage to Azure Blob Storage.
    This function is triggered by a timer or an HTTP request. It generates the
    HTML content for the webpage and uploads it to a specified Azure Blob Storage
    container using Managed Identity for authentication.
    """
    logging.info("Function triggered")
    # Use Managed Identity to upload the webpage to Azure Blob Storage
    upload_webpage_to_blob(
        storage_account_name=STORAGE_ACCOUNT_NAME,
        container_name=CONTAINER_NAME,
        blob_name="index.html"
    )
    # if HTTP request is made, return a success message
    if req:
        return func.HttpResponse(
            "Webpage uploaded successfully.",
            status_code=200
        )
    # if timer trigger, no HTTP response is needed
    logging.info("Webpage uploaded successfully.")
    return None

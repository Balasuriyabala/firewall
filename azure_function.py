import datetime
import requests
import os
from azure.storage.blob import BlobServiceClient
import logging

# Configuration
firewall_ip = "192.168.29.237"
api_key = "LUFRPT1OSEpnZG9OVVFaRWRXdkdHT1p2UmFWbnlCVUE9MkEzM3lDRzVYWkFmSW5Jd0JIdzFuVFZmd0hMTzR5M3ZGYzNlTS81NENnVGVGaWx3N3VMZS9wZXlYbi9sK1greA=="
backup_dir = r"/tmp/fwbackup"  # Temporary directory for backup (will work in Azure Functions environment)

# Azure Storage Configuration
azure_connection_string = "DefaultEndpointsProtocol=https;AccountName=backupfirewal;AccountKey=wMAp3EwGhJPLn5ryV8vzcG2YETTBgBjUY8LsS8OobJ/iMsmBLVIBvrmKxcmkOCMCwjIDpSQs/kLJ+AStWlQ29Q==;EndpointSuffix=core.windows.net"
container_name = "backup"

def main(mytimer: func.TimerRequest) -> None:
    """Timer Trigger function that runs every day at 10 AM."""
    
    logging.info('Starting firewall configuration backup...')
    current_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = os.path.join(backup_dir, f"paloalto_backup_{current_date}.xml")
    
    url = f"https://{firewall_ip}/api/?type=export&category=configuration&key={api_key}"
    
    try:
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            os.makedirs(backup_dir, exist_ok=True)
            with open(backup_file, "wb") as file:
                file.write(response.content)
            logging.info(f"Backup saved locally: {backup_file}")
            upload_to_azure_blob(backup_file, current_date)
        else:
            logging.error(f"Failed to download backup. Status code: {response.status_code}")
    except Exception as e:
        logging.error(f"An error occurred during backup: {e}")

def upload_to_azure_blob(file_path, timestamp):
    """Upload a file to Azure Blob Storage."""
    try:
        blob_service_client = BlobServiceClient.from_connection_string(azure_connection_string)
        file_name = os.path.basename(file_path)
        # Add timestamp to blob name
        blob_name = f"{os.path.splitext(file_name)[0]}_{timestamp}.xml"

        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data)
        logging.info(f"Backup uploaded to Azure Blob Storage: {blob_name}")
    except Exception as e:
        logging.error(f"An error occurred during Azure upload: {e}")

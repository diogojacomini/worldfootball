from shared_code.variables import COD_ERROR_PARAMETERS, CONNECTION_STRING
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


class AzureStore():

    def __init__(self) -> None:
        self.CONNECTION_STRING = CONNECTION_STRING
        self.connect()

    def connect(self):
        self.client = BlobServiceClient.from_connection_string(self.CONNECTION_STRING)

    def get_container(self, container_name):
        return self.client.get_container_client(container_name)

    def get_file(self, container_name, filename):
        return self.client.get_blob_client(container=container_name, blob=filename)

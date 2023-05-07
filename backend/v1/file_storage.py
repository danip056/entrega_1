from google.cloud import storage
from io import BytesIO
from abc import ABCMeta, abstractmethod
import os

BUCKET_NAME = os.environ.get("BUCKET_NAME", "dsc_08_bucket")
## Class factory for Storage. It has methos for reading and writing
## files 

class Storage:

    def  __init__(self, file_name, mode="rb"):
        self.file_name = file_name
        self.mode = mode

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, data):
        pass


class LocalStorage(Storage):
    def read(self):
        with open(self.file_name, self.mode) as file:
            return file.read()
    def write(self, data):
        with open(self.file_name, self.mode) as file:
            file.write(data)
    # Context manager for LocalStorage
    def __enter__(self):
        self.file = open(self.file_name, self.mode)
        return self.file
    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

class CloudStorage(Storage):
    
        def __init__(self, file_name, mode="rb", bucket_name=BUCKET_NAME):
            super().__init__(file_name, mode)
            self.bucket_name = bucket_name
            self.storage_client = storage.Client()
            self.bucket = self.storage_client.bucket(self.bucket_name)
            self.blob = self.bucket.blob(self.file_name)
    
        def read(self):
            return self.blob.download_as_bytes()
    
        def write(self, data):
            self.blob.upload_from_string(data)

        # Context manager for CloudStorage
        def __enter__(self):
            return self
        
        def __exit__(self, exc_type, exc_value, traceback):
            pass
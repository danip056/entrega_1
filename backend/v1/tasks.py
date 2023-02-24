from celery import shared_task
from compression import ZipManager, TarGzManager, TarBz2Manager, CompressionFormat
from bd_connection import Session
from models import Task
from api_models import Status
import os

STORAGE_DIR = "storage"

@shared_task(autoretry_for=(Exception,), max_retries=3 ,default_retry_delay=240, ignore_result=True)
def process_task(id_task):
    print("task id: {}".format(id_task))
    with Session() as session:
        task = session.query(Task).get(id_task)

        original_stored_file_name = task.original_stored_file_name
        original_file_ext = CompressionFormat(task.original_file_ext)
        target_stored_file_name = task.target_stored_file_name
        target_file_ext = CompressionFormat(task.target_file_ext)

        with open(os.path.join(
            STORAGE_DIR,
            original_stored_file_name,
        ), "rb") as original_file:

            if original_file_ext == CompressionFormat.ZIP:
                files_dict = ZipManager.decompress(original_file)
            elif original_file_ext == CompressionFormat.TAR_GZ:
                files_dict = TarGzManager.decompress(original_file)
            elif original_file_ext == CompressionFormat.TAR_BZ2:
                files_dict = TarBz2Manager.decompress(original_file)
            else:
                raise Exception("Unhandled file format")

        if target_file_ext == CompressionFormat.ZIP:
            target_file = ZipManager.compress(files_dict)
        elif target_file_ext == CompressionFormat.TAR_GZ:
            target_file = TarGzManager.compress(files_dict)
        elif target_file_ext == CompressionFormat.TAR_BZ2:
            target_file = TarBz2Manager.compress(files_dict)
        else:
            raise Exception("Unhandled file format")

        with open(os.path.join(
            STORAGE_DIR,
            target_stored_file_name,),
            "wb") as new_file:
            new_file.write(target_file)
            
        task.status = Status.PROCESSED.value
        session.commit()

        return None


from zipfile import ZipFile
from tarfile import TarFile, TarInfo
import tarfile
from enum import Enum
from io import BytesIO


class CompressionFormat(str, Enum):
    ZIP = ".zip"
    # S7Z = ".7z"
    # RAR = ".rar"
    # BZIP = ".bzip"
    TAR_GZ = ".tar.gz"
    TAR_BZ2 = ".tar.bz2"


# zip
class ZipManager:

    @classmethod
    def decompress(self, file):
        zip_file = ZipFile(file)
        return {name: zip_file.read(name) for name in zip_file.namelist()}

    @classmethod
    def compress(self, files_dict):
        compressed_zip = BytesIO()

        with ZipFile(compressed_zip, "w") as zf:
            for name,data in files_dict.items():
                zf.writestr(name, data)
        
        return compressed_zip.getvalue()

# tar.gz
class TarGzManager:

    @classmethod
    def decompress(self, file):
        with tarfile.open(fileobj=file, mode="r:gz") as tar_file:
            output = {name: tar_file.extractfile(name).read() for name in tar_file.getnames()}
        return output


    @classmethod
    def compress(self, files_dict):
        compressed_file = BytesIO()
        with tarfile.open(fileobj=compressed_file, mode='w:gz') as tf:
            for name,data in files_dict.items():
                file_tarinfo = TarInfo(name=name)
                file_tarinfo.size = len(data)
                data_buffer = BytesIO(data)
                tf.addfile(file_tarinfo, fileobj=data_buffer)

        return compressed_file.getvalue()

class TarBz2Manager:

    @classmethod
    def decompress(self, file):
        with tarfile.open(fileobj=file, mode="r:bz2") as tar_file:
            output = {name: tar_file.extractfile(name).read() for name in tar_file.getnames()}
        return output

    @classmethod
    def compress(self, files_dict):
        compressed_file = BytesIO()
        with tarfile.open(fileobj=compressed_file, mode='w:bz2') as tf:
            for name,data in files_dict.items():
                file_tarinfo = TarInfo(name=name)
                file_tarinfo.size = len(data)
                data_buffer = BytesIO(data)
                tf.addfile(file_tarinfo, fileobj=data_buffer)

        return compressed_file.getvalue()

# tar.bz2


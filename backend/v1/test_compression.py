import unittest
import os
from compression import ZipManager, TarGzManager, TarBz2Manager


TEST_CASES_PATH = os.path.join(
    os.path.dirname(__file__),
    "compression_cases",
)

class TestZipMethods(unittest.TestCase):

    def test_decompress(self):
        with open(os.path.join(TEST_CASES_PATH, "zip_case.zip"), "rb") as zip_file:
            files_dict = ZipManager.decompress(zip_file)
        self.assertDictEqual(
            files_dict,
            {'file_1.txt': b'ok 1!', 'file_2.txt': b'ok 2!'}
        )


    def test_compress_folder(self):

        walk_path = os.path.join(TEST_CASES_PATH, "compression_case_1")
        walker = os.walk(walk_path)

        files_dict = {}
        for current_path, _, files_names in walker:

            for file_name in files_names:
                file_path = os.path.join(current_path, file_name)
                file_relpath = os.path.relpath(
                    file_path,
                    walk_path
                )
                with open(file_path, "rb") as file:
                    files_dict[file_relpath] = file.read()
        zip_file = ZipManager.compress(files_dict)
        
class TestTarGzMethods(unittest.TestCase):

    def test_decompress(self):
        with open(os.path.join(TEST_CASES_PATH, "tar_case.tar.gz"), "rb") as tar_file:
            files_dict = TarGzManager.decompress(tar_file)
        self.assertDictEqual(
            files_dict,
            {
                'file_1.txt': b'compression ok 1!',
                'file_2.txt': b'compresssion ok 2!',
                os.path.join("wow","file_1.txt"):b'compression ok 1!',
            }
        )

    def test_compress_folder(self):

            walk_path = os.path.join(TEST_CASES_PATH, "compression_case_1")
            walker = os.walk(walk_path)

            files_dict = {}
            for current_path, _, files_names in walker:

                for file_name in files_names:
                    file_path = os.path.join(current_path, file_name)
                    file_relpath = os.path.relpath(
                        file_path,
                        walk_path
                    )
                    with open(file_path, "rb") as file:
                        files_dict[file_relpath] = file.read()
            tar_file = TarGzManager.compress(files_dict)


class TestTarBz2Methods(unittest.TestCase):

    def test_decompress(self):
        with open(os.path.join(TEST_CASES_PATH, "tar_case.tar.bz2"), "rb") as tar_file:
            files_dict = TarBz2Manager.decompress(tar_file)
        self.assertDictEqual(
            files_dict,
            {
                'file_1.txt': b'compression ok 1!',
                'file_2.txt': b'compresssion ok 2!',
                os.path.join("wow","file_1.txt"):b'compression ok 1!',
            }
        )

    def test_compress_folder(self):

            walk_path = os.path.join(TEST_CASES_PATH, "compression_case_1")
            walker = os.walk(walk_path)

            files_dict = {}
            for current_path, _, files_names in walker:

                for file_name in files_names:
                    file_path = os.path.join(current_path, file_name)
                    file_relpath = os.path.relpath(
                        file_path,
                        walk_path
                    )
                    with open(file_path, "rb") as file:
                        files_dict[file_relpath] = file.read()
            tar_file = TarBz2Manager.compress(files_dict)

if __name__ == '__main__':
    unittest.main()
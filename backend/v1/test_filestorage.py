import unittest
import os
import sys
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    os.path.dirname(BASE_DIR), "cloud_credentials.json")
sys.path.append(BASE_DIR)
from v1.file_storage import LocalStorage, CloudStorage

STORAGE_DIR = os.path.join(BASE_DIR, "storage_test")

class TestFileStorage(unittest.TestCase):
    def setUp(self):
        if not os.path.exists(STORAGE_DIR):
            os.mkdir(STORAGE_DIR)
        self.storage = LocalStorage(os.path.join(STORAGE_DIR, "test.txt"), "w")

    def test_write(self):
        self.storage = LocalStorage(os.path.join(STORAGE_DIR, "test.txt"), "w")
        self.storage.write("Hello world")
        with open(os.path.join(STORAGE_DIR, "test.txt"), "r") as file:
            self.assertEqual(file.read(), "Hello world")

    def test_read(self):
        self.storage = LocalStorage(os.path.join(STORAGE_DIR, "test.txt"), "r")
        with open(os.path.join(STORAGE_DIR, "test.txt"), "w") as file:
            file.write("Hello world")
        self.assertEqual(self.storage.read(), "Hello world")

    def tearDown(self):
        shutil.rmtree(STORAGE_DIR)

class TestCloudStorage(unittest.TestCase):
    def setUp(self):
        self.storage = CloudStorage("test.txt")
        self.storage.write("Hello world")

    def test_read(self):
        self.assertEqual(self.storage.read(), b"Hello world")

    def tearDown(self):
        self.storage.blob.delete()

if __name__ == "__main__":
    unittest.main()
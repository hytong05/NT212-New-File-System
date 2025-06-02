import unittest
from src.filesystem.myfs import MyFS

class TestMyFS(unittest.TestCase):

    def setUp(self):
        self.myfs = MyFS("test_volume.DRI")
        self.myfs.create_volume()

    def test_create_volume(self):
        self.assertTrue(self.myfs.volume_exists())

    def test_import_file(self):
        self.myfs.import_file("test_file.txt")
        self.assertIn("test_file.txt", self.myfs.list_files())

    def test_export_file(self):
        self.myfs.import_file("test_file.txt")
        self.myfs.export_file("test_file.txt", "exported_test_file.txt")
        self.assertTrue(os.path.exists("exported_test_file.txt"))

    def test_list_files(self):
        self.myfs.import_file("test_file.txt")
        files = self.myfs.list_files()
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0], "test_file.txt")

    def test_delete_file(self):
        self.myfs.import_file("test_file.txt")
        self.myfs.delete_file("test_file.txt")
        self.assertNotIn("test_file.txt", self.myfs.list_files())

    def tearDown(self):
        self.myfs.delete_volume()

if __name__ == '__main__':
    unittest.main()
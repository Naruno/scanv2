import contextlib
import time
import unittest
import os
import shutil
from scan import SCAN


class test_object:
    
    def exp(self):
        return {"test":"test"}

class TestKOT(unittest.TestCase):

    def setUp(self):

        SCAN.database_delete_all()

        self.test_name = "test_user"
        self.SCAN = SCAN(self.test_name)

        self.test_vales = ["Merhaba", 123, 123.213, {"test":"test"}, ["test", "test2"], ("test", "test2"), True, False, None]
        
    def tearDown(self):
        shutil.rmtree(self.SCAN.location)

    def test_set_get_delete(self):
        self.SCAN.set("key1", self.test_vales)
        self.assertEqual(self.SCAN.get("key1"), self.test_vales)
        self.assertEqual(self.SCAN.dict(), {"key1":self.test_vales})
        self.SCAN.delete("key1")
        self.assertEqual(self.SCAN.get("key1"), None)

    def test_set_get_delete_location(self):
        self.SCAN.set("key1", self.test_vales)
        self.assertEqual(self.SCAN.get("key1"), self.test_vales)
        # create a folder in the location if not exists
        currently_dir = os.getcwd()
        if not os.path.exists(currently_dir + "/test"):
            os.makedirs(currently_dir + "/test")
        
        false_kot = SCAN(self.test_name, folder=currently_dir + "/test")
        self.assertNotEqual(false_kot.get("key1"), self.test_vales)

        
        true_kot = SCAN(self.test_name, folder=currently_dir)
        self.assertEqual(true_kot.get("key1"), self.test_vales)        

    def test_set_get_delete_file(self):

        with open("test_file.txt", "w") as f:
            f.write("test")

        self.SCAN.set("key1", file="test_file.txt")
        self.assertEqual(os.path.exists("test_file.txt"), False)
        file_path = self.SCAN.get("key1")
        with open(file_path, "r") as f:
            self.assertEqual(f.read(), "test")
        self.SCAN.delete("key1")
        self.assertEqual(os.path.exists(file_path), False)

    def test_set_get_delete_file_compress(self):

        with open("test_file.txt", "w") as f:
            f.write("test")

        self.SCAN.set("key1", file="test_file.txt", compress=True)
        with open(self.SCAN.get("key1"), "r") as f:
            self.assertEqual(f.read(), "test")

    def test_set_get_delete_file_encryption(self):

        with open("test_file.txt", "w") as f:
            f.write("test")

        self.SCAN.set("key1", file="test_file.txt", encryption_key="Onur")
        with open(self.SCAN.get("key1", encryption_key="Onur"), "r") as f:
            self.assertEqual(f.read(), "test")

    def test_set_get_delete_file_compress_encryption(self):

        with open("test_file.txt", "w") as f:
            f.write("test")

        self.SCAN.set("key1", file="test_file.txt", compress=True, encryption_key="Onur")
        with open(self.SCAN.get("key1", encryption_key="Onur"), "r") as f:
            self.assertEqual(f.read(), "test")


    def test_set_get_delete_multiple(self):
        self.SCAN.set("key1", self.test_vales)
        self.SCAN.set("key2", self.test_vales)
        self.assertEqual(self.SCAN.get("key1"), self.test_vales)
        self.assertEqual(self.SCAN.get("key2"), self.test_vales)
        self.assertEqual(self.SCAN.dict(), {"key1":self.test_vales,"key2":self.test_vales})
        self.SCAN.delete("key1")
        self.assertEqual(self.SCAN.get("key1"), None)
        self.assertNotEqual(self.SCAN.get("key2"), None)
        self.SCAN.delete("key2")
        self.assertEqual(self.SCAN.get("key2"), None)

    def test_set_get_delete_object_compress_encryption(self):
        self.SCAN.set("key1", test_object(), compress=True, encryption_key="OnurAtakanULUSOY")
        self.assertEqual(self.SCAN.get("key1", encryption_key="OnurAtakanULUSOY").exp(), test_object().exp())
        the_dict = self.SCAN.dict(encryption_key="OnurAtakanULUSOY")
        the_dict["key1"] = the_dict["key1"].exp()
        self.assertEqual(the_dict, {"key1":test_object().exp()})
        self.SCAN.delete("key1")
        self.assertEqual(self.SCAN.get("key1"), None)


    def test_set_invalid_key(self):
        with self.assertRaises(TypeError):
            self.SCAN.set(123, "invalid_key")



    def test_set_withrkey_get_delete_without_key(self):
        key_name = self.SCAN.set_withrkey(self.test_vales)
        self.assertEqual(self.SCAN.get(key_name), self.test_vales)


    def test_set_get_delete_all(self):
        self.SCAN.set("key1", self.test_vales)
        self.assertEqual(self.SCAN.get("key1"), self.test_vales)
        self.SCAN.delete_all()
        self.assertEqual(self.SCAN.get("key1"), None)

    def test_set_get_no_compress(self):
        self.SCAN.set("key1", self.test_vales, compress=False)
        self.assertEqual(self.SCAN.get("key1"), self.test_vales)

    def test_set_get_yes_compress(self):
        self.SCAN.set("key1", self.test_vales, compress=True)
        self.assertEqual(self.SCAN.get("key1"), self.test_vales)



    def test_set_get_size(self):
        self.SCAN.set("key1", self.test_vales, compress=True)
        the_size_of_value = self.SCAN.size("key1")
        self.assertGreater(the_size_of_value, 0)


    def test_set_get_compress_test(self):

        big_string = "a" * 1000000


        self.SCAN.set("key1", big_string, compress=False)
        the_size_of_not_compress = self.SCAN.size_all()
        self.SCAN.delete_all()
        
        self.SCAN.set("key1", big_string, compress=True)
        the_size_of_compress = self.SCAN.size_all()
        self.SCAN.delete_all()

        self.assertGreater(the_size_of_not_compress, the_size_of_compress)


    def test_set_get_compress_test_file_and_dont_remove_file(self):

        big_string = "a" * 1000000
        with open("test_file.txt", "w") as f:
            f.write(big_string)


        self.SCAN.set("key1", file="test_file.txt", compress=False, dont_remove_file=True)
        the_size_of_not_compress = self.SCAN.size_all()
        self.SCAN.delete_all()

        self.assertNotEqual(self.SCAN.get("key1"), False)
        
        self.assertEqual(self.SCAN.set("key1", file="test_file.txt", compress=True) , True)
        the_size_of_compress = self.SCAN.size_all()
        self.SCAN.delete_all()

        self.assertGreater(the_size_of_not_compress, the_size_of_compress)

    def test_set_get_compress_encyrption_test(self):

        big_string = "a" * 1000000
        self.SCAN.set("key1", big_string, compress=True, encryption_key="OnurAtakanULUSOY")
        self.assertEqual(self.SCAN.get("key1", encryption_key="OnurAtakanULUSOY"), big_string)



    def test_set_get_delete_encryption_decryption(self):
        self.SCAN.set("key1", self.test_vales, encryption_key="OnurAtakanULUSOY")

        self.assertNotEqual(self.SCAN.get("key1"), self.test_vales)

        self.assertEqual(self.SCAN.get("key1", encryption_key="OnurAtakanULUSOY"), self.test_vales)

        self.assertNotEqual(self.SCAN.dict(), {"key1":self.test_vales})
        self.assertEqual(self.SCAN.dict(encryption_key="OnurAtakanULUSOY"), {"key1":self.test_vales})



    def test_set_get_delete_cache(self):
        self.SCAN.set("key1", self.test_vales, cache_policy=30)
        self.assertEqual(self.SCAN.get("key1"), self.test_vales)
        self.SCAN.set("key1", "value1aaaa", dont_delete_cache=True)
        self.assertEqual(self.SCAN.get("key1"), self.test_vales)
        self.SCAN.set("key1", "value1aaaa", dont_delete_cache=False)
        self.assertEqual(self.SCAN.get("key1"), "value1aaaa")


    def test_set_get_delete_cache_expired(self):
        self.SCAN.set("key1", self.test_vales, cache_policy=1)
        self.assertEqual(self.SCAN.get("key1"), self.test_vales)
        self.SCAN.set("key1", "value1aaaa", dont_delete_cache=True)
        time.sleep(4)
        self.assertEqual(self.SCAN.get("key1"), "value1aaaa")

    def test_set_get_delete_cache_no_cache(self):
        self.SCAN.set("key1", self.test_vales, cache_policy=30)
        self.assertEqual(self.SCAN.get("key1"), self.test_vales)
        self.SCAN.set("key1", "value1aaaa", dont_delete_cache=True)
        self.assertEqual(self.SCAN.get("key1", no_cache=True), "value1aaaa")

    def test_set_get_delete_cache_clear_cache(self):


        with open("test_file.txt", "w") as f:
            f.write("test")
        self.SCAN.set("key1", file="test_file.txt")
        self.assertEqual(os.path.exists("test_file.txt"), False)
        file_path = self.SCAN.get("key1")
        with open(file_path, "r") as f:
            self.assertEqual(f.read(), "test")
        

        self.SCAN.set("key1", self.test_vales, cache_policy=15)
        self.assertEqual(self.SCAN.get("key1"), self.test_vales)
        self.SCAN.set("key1", "value1aaaa", dont_delete_cache=True)
        self.SCAN.clear_cache()
        self.assertEqual(self.SCAN.get("key1"), "value1aaaa")
        self.assertEqual(os.path.exists(file_path), False)


    def test_backup_restore(self):
        self.SCAN.set("key1", self.test_vales)
        self.assertEqual(self.SCAN.get("key1"), self.test_vales)
        backup_location = self.SCAN.backup("test_backup")

        another_kp = SCAN("backup_test")
        another_kp.delete_all()

        self.assertEqual(another_kp.get("key1"), None)
        result_of_restore = another_kp.restore(backup_location)
        self.assertTrue(result_of_restore)
        self.assertEqual(another_kp.get("key1"), self.test_vales)


    def test_database_list_delete_delete_all(self):
        backup_chdir = os.getcwd()
        the_time = str(int(time.time()))
        os.makedirs(os.path.join(self.SCAN.location, the_time))
        os.chdir(os.path.join(self.SCAN.location, the_time))
        database_list = SCAN.database_list()

        self.assertEqual(database_list, {})
        a_new_kp = SCAN("test_database_list")
        database_list = SCAN.database_list()

        self.assertEqual(database_list, {"test_database_list":a_new_kp.location})
        a_new_other_kp = SCAN("test_database_list2")
        database_list = SCAN.database_list()

        self.assertEqual(database_list, {"test_database_list":a_new_kp.location, "test_database_list2":a_new_other_kp.location})

        SCAN.database_delete("test_database_list2")

        database_list = SCAN.database_list()

        self.assertEqual(database_list, {"test_database_list":a_new_kp.location})

        a_new_other_kp = SCAN("test_database_list2")


        SCAN.database_delete_all()

        database_list = SCAN.database_list()

        self.assertEqual(database_list, {})

        with contextlib.suppress(PermissionError):
            shutil.rmtree(os.path.join(self.SCAN.location, the_time))


        os.chdir(backup_chdir)


    def test_database_rename_already(self):
        first_db = SCAN("firstdb")
        first_db.set("key1", self.test_vales)
        self.assertEqual(first_db.get("key1"), self.test_vales)
        new_db = SCAN("test_database_rename_already")
        new_db.delete_all()
        self.assertNotEqual(new_db.get("key1"), self.test_vales)
        result = SCAN.database_rename("firstdb", "test_database_rename_already")
        self.assertFalse(result)


    def test_database_rename_force(self):
        first_db = SCAN("firstdb")
        first_db.set("key1", self.test_vales)
        self.assertEqual(first_db.get("key1"), self.test_vales)
        new_db = SCAN("test_database_rename_already")
        new_db.delete_all()
        self.assertNotEqual(new_db.get("key1"), self.test_vales)
        result = SCAN.database_rename("firstdb", "test_database_rename_already", True)
        self.assertTrue(result)
        self.assertEqual(first_db.get("key1"), None)
        self.assertEqual(new_db.get("key1"), self.test_vales)
        
    def test_database_rename(self):
        first_db = SCAN("firstdb")
        first_db.set("key1", self.test_vales)
        self.assertEqual(first_db.get("key1"), self.test_vales)
        SCAN.database_delete("test_database_rename_already")
        result = SCAN.database_rename("firstdb", "test_database_rename_already",)
        self.assertTrue(result)
        self.assertEqual(first_db.get("key1"), None)
        self.assertEqual(SCAN("test_database_rename_already").get("key1"), self.test_vales)



    def test_dict_no_data(self):
        self.SCAN.set("key1", self.test_vales)
        self.assertEqual(self.SCAN.get("key1"), self.test_vales)
        self.assertEqual(self.SCAN.dict(no_data=True), {"key1":True})
        self.SCAN.delete("key1")
        self.assertEqual(self.SCAN.get("key1"), None)        


if __name__ == '__main__':
    unittest.main()

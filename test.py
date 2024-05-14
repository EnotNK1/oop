import unittest
from userservice.userservice import user_service
from database.database import database_service

class Test(unittest.TestCase):

    def test_auth(self):
        self.assertEqual(user_service.authorization("wowova@bk.ru", "321"), "error")
        self.assertEqual(user_service.reset_password("wowo@bk.ru"), "No user with this e-mail account was found")

    def test_reg(self):
        self.assertEqual(user_service.register("wowova@bk.ru", "12345", "12345"),
                         "A email address has already been registered")
        self.assertEqual(user_service.register("fdgdfg@bk.ru", "123455", "12345"), "Password mismatch")


    def test_add_phrase(self):
        self.assertEqual(user_service.add_phrase("dfgdfg@bk.ru", "dfgh", "dfgh"), "error")

    def test_del_phrase(self):
        self.assertEqual(user_service.deleet_phrase("wowova@bk.ru", "gfgfgf", "gfgfgf"), "not have")
        self.assertEqual(user_service.deleet_phrase("dfdfgfdg@mail.ru", "111", "111"), "not have")

    def test_check_word(self):
        self.assertEqual(database_service.check_phrase("fuuga@mail.ru", "word", "word"), -1)


unittest.main()
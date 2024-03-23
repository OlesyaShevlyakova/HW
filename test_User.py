import unittest
from User import User
from Utils import hash_password as hs

class TestItem(unittest.TestCase):
    def test_init_user(self):
        "Проверка создания пользователя - стандартно"
        user1 = User("test_login", "test_name", "test_lastname", "test_password")
        self.assertEqual(user1._login, "test_login")
        self.assertEqual(user1._name, "test_name")
        self.assertEqual(user1._lastname, "test_lastname")
        self.assertEqual(user1._password, hs("test_password"))

    def test_init_user_hash_pass(self):
        "Проверка создания пользователя - с хешированным паролем"
        test_password_hash = '10a6e6cc8311a3e2bcc09bf6c199adecd5dd59408c343e926b129c4914f3cb01'
        user1 = User("test_login", "test_name", "test_lastname", hash_pass=test_password_hash)
        self.assertEqual(user1._login, "test_login")
        self.assertEqual(user1._name, "test_name")
        self.assertEqual(user1._lastname, "test_lastname")
        self.assertEqual(user1._password, test_password_hash)

    def test_init_user_check_id_counter(self):
        "Проверка работы счетчика при создании нескольких пользователей"
        id_counter_before_creating = User.__id_counter__
        test_password_hash = '10a6e6cc8311a3e2bcc09bf6c199adecd5dd59408c343e926b129c4914f3cb01'
        user1 = User("test_login", "test_name", "test_lastname", hash_pass=test_password_hash)
        user2 = User("test_login1", "test_name1", "test_lastname1", hash_pass=test_password_hash)
        user3 = User("test_login2", "test_name2", "test_lastname2", password="test_password2")
        user4 = User("test_login3", "test_name3", "test_lastname3", password="test_password3")
        self.assertEqual(user1._id, "@" + user1._name + user1._lastname + "*" + str(id_counter_before_creating))
        id_counter_before_creating += 1
        self.assertEqual(user2._id, "@" + user2._name + user2._lastname + "*" + str(id_counter_before_creating))
        id_counter_before_creating += 1
        self.assertEqual(user3._id, "@" + user3._name + user3._lastname + "*" + str(id_counter_before_creating))
        id_counter_before_creating += 1
        self.assertEqual(user4._id, "@" + user4._name + user4._lastname + "*" + str(id_counter_before_creating))

    def test_init_user_check_create_id(self):
        "Проверка работы присвоения id"
        user1 = User("test_login", "test_name", "test_lastname", "test_password3",
                     id='testid')
        self.assertEqual(user1._id, "testid")

    def test_info_User(self):
        "Проверка возврата информации о пользователе"
        id = "test_id"
        login = "test_login"
        name = "test_name"
        lastname = "test_lastname"
        password = "test_password"
        hash_password = hs(password)
        user1 = User(id=id, login=login, name=name, lastname=lastname, password=password)
        self.assertEqual(user1.info_User(),(id, name, lastname, login, hash_password ))

    def test_info_id_User(self):
        "Проверка возврата id пользователя"
        id = "test_id"
        login = "test_login"
        name = "test_name"
        lastname = "test_lastname"
        password = "test_password"
        hash_password = hs(password)
        user1 = User(id=id, login=login, name=name, lastname=lastname, password=password)
        self.assertEqual(user1.info_id_User(),id)

    def test_change_user(self):
        'Првоерка изменения данных о пользователе'
        password = "test_password"
        hash_password = hs(password)
        new_name = 'new_name'
        new_lastname = 'new_lastname'
        new_password = 'new_password'
        user1 = User("test_login1", "test_name1", "test_lastname1", password=password)
        user2 = User("test_login2", "test_name2", "test_lastname2", password=password)
        user3 = User("test_login3", "test_name3", "test_lastname3", password=password)
        user4 = User("test_login4", "test_name4", "test_lastname4", password=password)
        user1.change_user(new_name=new_name)
        user2.change_user(new_lastname=new_lastname)
        user3.change_user(new_password=new_password)
        user4.change_user(new_name=new_name, new_lastname=new_lastname, new_password=new_password)
        self.assertEqual(user1.info_User()[1], new_name)
        self.assertEqual(user2.info_User()[2], new_lastname)
        self.assertEqual(user3.info_User()[4], hs(new_password))
        self.assertEqual(user4.info_User()[1], new_name)
        self.assertEqual(user4.info_User()[2], new_lastname)
        self.assertEqual(user4.info_User()[4], hs(new_password))

    def test_str(self):
        'Проверка __str__'
        user1 = User("test_login1", "test_name1", "test_lastname1", password='new_password')
        self.assertEqual(str(user1),f"Пользователь {user1._login} с id {user1._id}")

    def test_repr(self):
        'Проверка __repr__'
        user1 = User("test_login1", "test_name1", "test_lastname1", password='new_password')
        self.assertEqual(user1.__repr__(),f"[{user1._login}:{user1._id}]")


    def test_change_id_counter(self):
        old_counter = User.__id_counter__
        new_counter = 456
        User.change_id_counter(new_counter)
        self.assertTrue(User.__id_counter__ == new_counter)
        self.assertTrue(User.__id_counter__ != old_counter)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

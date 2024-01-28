import unittest
from Backend import Backend
from User import User
from Event import Event
from Calendar import Calendar
from datetime import datetime
import csv
import shutil
from Utils import hash_password as hs





class MyTestCase(unittest.TestCase):
    Backend._directory = 'test_data/'
    def test_add_user(self):
        "Добавляет пользователя"
        Backend.list_users = []
        user1 = User("test_login1", "test_name1", "test_lastname1", password='new_password')
        Backend.add_user(user1)
        self.assertEqual(Backend.list_users[0], user1)  # add assertion here

    def test_originality_login(self):
        """Проверяем логин на уникальность"""
        self.assertFalse(Backend.originality_login('user1'))
        self.assertTrue(Backend.originality_login('user5'))

    def test_info_users_empty(self):
        "Возвращает информацию об пользователях - ПУСТО"
        Backend.list_users = []
        self.assertEqual(Backend.info_users(),[])

    def test_info_users_full(self):
        "Возвращает информацию об пользователях - С ДАННЫМИ"
        Backend.list_users = []
        user1 = User("test_login1", "test_name1", "test_lastname1", password='123')
        user2 = User("test_login2", "test_name2", "test_lastname2", password='123')
        Backend.add_user(user1)
        Backend.add_user(user2)
        self.assertEqual(Backend.info_users(),[user1,user2])
    def test_add_event(self):
        "Добавляет событие"
        ev1 = Event("event1", "event1_descr", "event1_own",
                    ["user1", "user2"], datetime(2007, 12, 6))
        ev2 = Event("event2", "event2_descr", "event2_own",
                    ["user3", "user4"], datetime(2008, 10, 16))
        Backend.list_events = []
        Backend.add_event(ev1)
        Backend.add_event(ev2)
        self.assertEqual(Backend.list_events,[ev1,ev2])

    def test_info_events_empty(self):
        "Возвращает информацию о событиях - ПУСТО"
        Backend.list_events = []
        self.assertEqual(Backend.info_events(),[])

    def test_info_events_full(self):
        "Возвращает информацию о событиях - С ДАННЫМИ"
        ev1 = Event("event1", "event1_descr", "event1_own",
                    ["user1", "user2"], datetime(2007, 12, 6))
        ev2 = Event("event2", "event2_descr", "event2_own",
                    ["user3", "user4"], datetime(2008, 10, 16))
        Backend.list_events = []
        Backend.add_event(ev1)
        Backend.add_event(ev2)
        self.assertEqual(Backend.info_events(),[ev1,ev2])

    def test_add_calendar(self):
        "Добавляет календарь"
        cal1 = Calendar('iduser1','work')
        cal2 = Calendar('iduser1','work')
        Backend.list_calendars=[]
        Backend.add_calendar(cal1)
        Backend.add_calendar(cal2)
        self.assertEqual(Backend.list_calendars,[cal1,cal2])

    def test_info_calendars_empty(self):
        "Возвращает информацию о календарях - ПУСТО"
        Backend.list_calendars=[]
        self.assertEqual(Backend.info_calendars(),[])

    def test_info_calendars_full(self):
        "Возвращает информацию о календарях - С ДАННЫМИ"
        cal1 = Calendar('iduser1', 'work')
        cal2 = Calendar('iduser1', 'work')
        Backend.list_calendars = []
        Backend.add_calendar(cal1)
        Backend.add_calendar(cal2)
        self.assertEqual(Backend.info_calendars(),[cal1,cal2])

    def test_add_event_into_calendar(self):
        "Добавляет событие в календарь"
        shutil.copyfile(Backend._directory + 'saved_calendars_etalon.txt', Backend._directory + 'saved_calendars.txt')
        cal1 = Calendar('iduser1', 'work', id=1)
        cal2 = Calendar('iduser2', 'personal', id=2)
        ev1 = Event("event1", "event1_descr", "event1_own",
                    ["user1", "user2"], datetime(2007, 12, 6), id=1)
        ev2 = Event("event2", "event2_descr", "event2_own",
                    ["user3", "user4"], datetime(2008, 10, 16), id=1)
        Backend.list_calendars = []
        Backend.list_events = []
        Backend.add_calendar(cal1)
        Backend.add_calendar(cal2)
        Backend.add_event(ev1)
        Backend.add_event(ev2)
        Backend.add_event_into_calendar('2','2')
        self.assertEqual(Backend.list_calendars[1]._events,['2'])
        file_name = Backend._directory + 'saved_calendars.txt'
        with open(file_name, "r") as f:
            w = csv.DictReader(f, ["id", "name_calendar", "id_user", "id_events"])
            next(w)
            next(w)
            for_check = (next(w)["id_events"])
        self.assertEqual(for_check,"['2']")
        shutil.copyfile(Backend._directory + 'saved_calendars_etalon.txt', Backend._directory + 'saved_calendars.txt')

    def test_save_file_calendars_write(self):
        """Создает файл с информацией о календарях - ПЕРЕЗАПИСЬ"""
        shutil.copyfile(Backend._directory + 'saved_calendars_clear.txt', Backend._directory + 'saved_calendars.txt')
        cal1 = Calendar('iduser1', 'work', id='1')
        cal2 = Calendar('iduser2', 'work', id='2')
        Backend.list_calendars = []
        Backend.add_calendar(cal1)
        Backend.add_calendar(cal2)
        Backend.save_file_calendars()
        file_name = Backend._directory + 'saved_calendars.txt'
        with open(file_name, "r") as f:
            w = csv.DictReader(f, ["id", "name_calendar", "id_user", "id_events"])
            next(w)
            first_row = next(w)
            second_row = next(w)
        self.assertEqual(first_row,{'id': '1', 'name_calendar': 'work', 'id_user': 'iduser1',
                                    'id_events': "[]"})
        self.assertEqual(second_row,{'id': '2', 'name_calendar': 'work', 'id_user': 'iduser2',
                                    'id_events': "[]"})
        shutil.copyfile(Backend._directory + 'saved_calendars_etalon.txt', Backend._directory + 'saved_calendars.txt')

    def test_save_file_calendars_append(self):
        """Создает файл с информацией о календарях - ДОЗАПИСЬ"""
        shutil.copyfile(Backend._directory + 'saved_calendars_clear.txt', Backend._directory + 'saved_calendars.txt')
        cal1 = Calendar('iduser1', 'work', id='1')
        cal2 = Calendar('iduser2', 'work', id='2')
        cal3 = Calendar('iduser3', 'work', id='3')
        Backend.list_calendars = []
        Backend.add_calendar(cal1)
        Backend.add_calendar(cal2)
        Backend.save_file_calendars()
        Backend.list_calendars = []
        Backend.add_calendar(cal3)
        Backend.save_file_calendars(add_calendar=True)
        file_name = Backend._directory + 'saved_calendars.txt'
        with open(file_name, "r") as f:
            w = csv.DictReader(f, ["id", "name_calendar", "id_user", "id_events"])
            next(w)
            first_row = next(w)
            second_row = next(w)
            third_row = next(w)
        self.assertEqual(first_row, {'id': '1', 'name_calendar': 'work', 'id_user': 'iduser1',
                                     'id_events': "[]"})
        self.assertEqual(second_row, {'id': '2', 'name_calendar': 'work', 'id_user': 'iduser2',
                                      'id_events': "[]"})
        self.assertEqual(third_row, {'id': '3', 'name_calendar': 'work', 'id_user': 'iduser3',
                                      'id_events': "[]"})
        shutil.copyfile(Backend._directory + 'saved_calendars_etalon.txt', Backend._directory + 'saved_calendars.txt')


    def test_load_file_calendars_all(self):
        """Загружаем календарь из файла - ВСЕХ"""
        shutil.copyfile(Backend._directory + 'saved_calendars_etalon.txt', Backend._directory + 'saved_calendars.txt')
        Backend.load_file_calendars()
        part1 = Backend.list_calendars[0]._id+Backend.list_calendars[0]._name_calendar
        part2 = Backend.list_calendars[0]._id_user+str(Backend.list_calendars[0]._events)
        self.assertEqual("1workiduser1['1', '2']",part1+part2)
        part1 = Backend.list_calendars[1]._id+Backend.list_calendars[1]._name_calendar
        part2 = Backend.list_calendars[1]._id_user+str(Backend.list_calendars[1]._events)
        self.assertEqual("2personaliduser2['3']",part1+part2)
        part1 = Backend.list_calendars[2]._id+Backend.list_calendars[2]._name_calendar
        part2 = Backend.list_calendars[2]._id_user+str(Backend.list_calendars[2]._events)
        self.assertEqual("3vacationiduser3['1', '2', '3']",part1+part2)

    def test_load_file_calendars_one(self):
        """Загружаем календарь из файла - ОДИН"""
        shutil.copyfile(Backend._directory + 'saved_calendars_etalon.txt', Backend._directory + 'saved_calendars.txt')
        Backend.load_file_calendars('iduser2')
        part1 = Backend.list_calendars[0]._id+Backend.list_calendars[0]._name_calendar
        part2 = Backend.list_calendars[0]._id_user+str(Backend.list_calendars[0]._events)
        self.assertEqual("2personaliduser2['3']",part1+part2)

    def test_load_file_calendars_max_counter(self):
        """Загружаем календарь из файла - КАУНТЕР"""
        shutil.copyfile(Backend._directory + 'saved_calendars_etalon.txt', Backend._directory + 'saved_calendars.txt')
        Calendar.__id_counter__=1
        Backend.load_file_calendars('*********')
        self.assertEqual(Calendar.__id_counter__,4)

    def test_clear_users(self):
        "Очищаем список пользователей"
        Backend.list_users = []
        user1 = User("test_login1", "test_name1", "test_lastname1", password='123')
        user2 = User("test_login2", "test_name2", "test_lastname2", password='123')
        Backend.add_user(user1)
        Backend.add_user(user2)
        Backend.clear_users()
        self.assertEqual(Backend.list_users,[])

    def test_clear_calendars(self):
        "Очищаем список календарей"
        Backend.list_calendars = []
        cal1 = Calendar('iduser1', 'work', id='1')
        cal2 = Calendar('iduser2', 'work', id='2')
        Backend.list_calendars = []
        Backend.add_calendar(cal1)
        Backend.add_calendar(cal2)
        Backend.clear_calendars()
        self.assertEqual(Backend.list_calendars,[])

    def test_clear_events(self):
        "Очищаем список событий"
        Backend.list_users = []
        ev1 = Event("event1", "event1_descr", "event1_own",
                    ["user1", "user2"], datetime(2007, 12, 6), id=1)
        ev2 = Event("event2", "event2_descr", "event2_own",
                    ["user3", "user4"], datetime(2008, 10, 16), id=1)
        Backend.list_events = []
        Backend.add_event(ev1)
        Backend.add_event(ev2)
        Backend.clear_events()
        self.assertEqual(Backend.list_events,[])

    def test_update_user(self):
        "Метод обновления пользователя:"
        shutil.copyfile(Backend._directory + 'saved_users_etalon.txt', Backend._directory + 'saved_users.txt')
        Backend.update_user('user3','new_name','new_lastname','new_pass')
        file_name = Backend._directory + 'saved_users.txt'
        with open(file_name, "r") as f:
            w = csv.DictReader(f, ["id","name","lastname","login","password"])
            next(w)
            next(w)
            next(w)
            for_check = next(w)
            for_check = for_check["name"]+for_check["lastname"]+for_check["password"]
        self.assertEqual(for_check, "new_namenew_lastname"+hs('new_pass'))
        shutil.copyfile(Backend._directory + 'saved_users_etalon.txt', Backend._directory + 'saved_users.txt')

    def test_update_calendar(self):
        "Метод обновления имени календаря"
        shutil.copyfile(Backend._directory + 'saved_calendars_etalon.txt', Backend._directory + 'saved_calendars.txt')
        Backend.update_calendar('2','new_name')
        file_name = Backend._directory + 'saved_calendars.txt'
        with open(file_name, "r") as f:
            w = csv.DictReader(f, ["id", "name_calendar", "id_user", "id_events"])
            next(w)
            first_row = next(w)
            second_row = next(w)
            third_row = next(w)
        self.assertEqual(first_row, {'id': '1', 'name_calendar': 'work', 'id_user': 'iduser1',
                                     'id_events': "['1', '2']"})
        self.assertEqual(second_row, {'id': '2', 'name_calendar': 'new_name', 'id_user': 'iduser2',
                                      'id_events': "[]"})
        self.assertEqual(third_row, {'id': '3', 'name_calendar': 'vacation', 'id_user': 'iduser3',
                                     'id_events': "['1', '2', '3']"})
        shutil.copyfile(Backend._directory + 'saved_calendars_etalon.txt', Backend._directory + 'saved_calendars.txt')

    def test_check_id_calendar(self):
        "Проверяем присутствие id календаря в памяти"
        shutil.copyfile(Backend._directory + 'saved_calendars_etalon.txt', Backend._directory + 'saved_calendars.txt')
        Backend.load_file_calendars()
        self.assertTrue(Backend.check_id_calendar('2'))
        self.assertFalse(Backend.check_id_calendar('5'))

    def test_check_id_users(self):
        "Проверяем присутствие id пользователей в памяти"
        shutil.copyfile(Backend._directory + 'saved_users_etalon.txt', Backend._directory + 'saved_calendars.txt')
        Backend.load_file_users()
        self.assertTrue(Backend.check_id_users(['@user3*3']))
        self.assertFalse(Backend.check_id_users(['5']))

    def test_check_id_event(self):
        "Проверяем присутствие id события в памяти"
        shutil.copyfile(Backend._directory + 'saved_events_etalon.txt', Backend._directory + 'saved_events.txt')
        Backend.load_file_events()
        self.assertTrue(Backend.check_id_event('1'))
        self.assertFalse(Backend.check_id_event('5'))

#TODO: load\save users, load\save events, load\save notifications
#TODO: show_events, search_events, add_event_into_calendar_guest, del_event_from_calendars
#TODO: clear_notification, add_notification, check_id_notification, info_notifications

if __name__ == '__main__':
    unittest.main()

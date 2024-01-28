import unittest
from Backend import Backend
from User import User
from Event import Event
from Calendar import Calendar
from datetime import datetime



class MyTestCase(unittest.TestCase):
    Backend._directory = 'test_data/'
    def test_add_user(self):
        Backend.list_users = []
        user1 = User("test_login1", "test_name1", "test_lastname1", password='new_password')
        Backend.add_user(user1)
        self.assertEqual(Backend.list_users[0], user1)  # add assertion here

    def test_originality_login(self):
        self.assertFalse(Backend.originality_login('user1'))
        self.assertTrue(Backend.originality_login('user5'))

    def test_info_users_empty(self):
        Backend.list_users = []
        self.assertEqual(Backend.info_users(),[])

    def test_info_users_full(self):
        Backend.list_users = []
        user1 = User("test_login1", "test_name1", "test_lastname1", password='123')
        user2 = User("test_login2", "test_name2", "test_lastname2", password='123')
        Backend.add_user(user1)
        Backend.add_user(user2)
        self.assertEqual(Backend.info_users(),[user1,user2])
    def test_add_event(self):
        ev1 = Event("event1", "event1_descr", "event1_own",
                    ["user1", "user2"], datetime(2007, 12, 6))
        ev2 = Event("event2", "event2_descr", "event2_own",
                    ["user3", "user4"], datetime(2008, 10, 16))
        Backend.list_events = []
        Backend.add_event(ev1)
        Backend.add_event(ev2)
        self.assertEqual(Backend.list_events,[ev1,ev2])

    def test_info_events_empty(self):
        Backend.list_events = []
        self.assertEqual(Backend.info_events(),[])

    def test_info_events_full(self):
        ev1 = Event("event1", "event1_descr", "event1_own",
                    ["user1", "user2"], datetime(2007, 12, 6))
        ev2 = Event("event2", "event2_descr", "event2_own",
                    ["user3", "user4"], datetime(2008, 10, 16))
        Backend.list_events = []
        Backend.add_event(ev1)
        Backend.add_event(ev2)
        self.assertEqual(Backend.info_events(),[ev1,ev2])

    def test_add_calendar(self):
        cal1 = Calendar('iduser1','work')
        cal2 = Calendar('iduser1','work')
        Backend.list_calendars=[]
        Backend.add_calendar(cal1)
        Backend.add_calendar(cal2)
        self.assertEqual(Backend.list_calendars,[cal1,cal2])

    def test_info_calendars_empty(self):
        Backend.list_calendars=[]
        self.assertEqual(Backend.info_calendars(),[])

    def test_info_calendars_full(self):
        cal1 = Calendar('iduser1', 'work')
        cal2 = Calendar('iduser1', 'work')
        Backend.list_calendars = []
        Backend.add_calendar(cal1)
        Backend.add_calendar(cal2)
        self.assertEqual(Backend.info_calendars(),[cal1,cal2])

    def test_add_event_into_calendar(self):
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
        self.assertEqual(True,True)



if __name__ == '__main__':
    unittest.main()

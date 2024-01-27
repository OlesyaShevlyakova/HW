import unittest
from Event import Event
from datetime import datetime


class MyTestCase(unittest.TestCase):
    def test_init_event(self):
        "Проверка создания ивента - стандартно"
        ev1 = Event("event1", "event1_descr", "event1_own",
                    ["user1", "user2"], datetime(2007, 12, 6))
        self.assertEqual(ev1._name_event, 'event1')
        self.assertEqual(ev1._description, 'event1_descr')
        self.assertEqual(ev1._event_owner, 'event1_own')
        self.assertEqual(ev1._event_guests,["user1", "user2"])
        self.assertEqual(ev1._data_event, datetime(2007, 12, 6))

    def test_init_calendar_custom(self):
        "Проверка создания ивента - с доп.параметрами"
        ev1 = Event("event1", "event1_descr", "event1_own",
                    ["user1", "user2"], datetime(2007, 12, 6),
                    repeat_type='D',id='id1')
        self.assertEqual(ev1._name_event, 'event1')
        self.assertEqual(ev1._description, 'event1_descr')
        self.assertEqual(ev1._event_owner, 'event1_own')
        self.assertEqual(ev1._event_guests,["user1", "user2"])
        self.assertEqual(ev1._data_event, datetime(2007, 12, 6))
        self.assertEqual(ev1._repeat_type, 'D')
        self.assertEqual(ev1._id,'id1')


    def test_init_calendar_check_id_counter(self):
        "Проверка работы счетчика при создании нескольких ивентов"
        id_counter_before_creating = Event.__id_counter__

        ev1 = Event("event1", "event1_descr", "event1_own",
                    ["user1", "user2"], datetime(2007, 12, 6))
        ev2 = Event("event2", "event2_descr", "event2_own",
                    ["user3", "user4"], datetime(2008, 10, 16))
        ev3 = Event("event3", "event3_descr", "event3_own",
                    ["user5", "user6"], datetime(2009, 11, 26))
        self.assertEqual(ev1._id, id_counter_before_creating)
        id_counter_before_creating += 1
        self.assertEqual(ev2._id, id_counter_before_creating)
        id_counter_before_creating += 1
        self.assertEqual(ev3._id, id_counter_before_creating)

    def test_info_Event(self):
        "Проверка - Возвращает информацию об Event"
        ev1 = Event("event1", "event1_descr", "event1_own",
                    ["user1", "user2"], datetime(2007, 12, 6),
                    repeat_type='D', id='id1')
        self.assertEqual(ev1.info_Event(), ( 'id1', "event1", "event1_descr",
                                             datetime(2007, 12, 6), 'D',
                                             "event1_own", ["user1", "user2"]))
    def test_info_data_event(self):
        "Проверка - Возвращает информацию о дате Event"
        ev1 = Event("event1", "event1_descr", "event1_own",
                    ["user1", "user2"], datetime(2007, 12, 6),
                    repeat_type='D', id='id1')
        self.assertEqual(ev1.info_data_event(), datetime(2007, 12, 6))

    def test_info_id_event(self):
        "Проверка - Возвращает информацию об id Event"
        ev1 = Event("event1", "event1_descr", "event1_own",
                    ["user1", "user2"], datetime(2007, 12, 6),
                    repeat_type='D', id='id1')
        self.assertEqual(ev1._id, 'id1')

    def test_change_name_event(self):
        "Проверка - Замена названия Event"
        ev1 = Event("event1", "event1_descr", "event1_own",
                    ["user1", "user2"], datetime(2007, 12, 6),
                    repeat_type='D', id='id1')
        ev1.change_name_event('new_name1')
        self.assertEqual(ev1._name_event, 'new_name1')

    def test_change_description(self):
        "Проверка - Замена описания Event"
        ev1 = Event("event1", "event1_descr", "event1_own",
                    ["user1", "user2"], datetime(2007, 12, 6),
                    repeat_type='D', id='id1')
        ev1.change_description('new_descr1')
        self.assertEqual(ev1._description, 'new_descr1')

    def test_add_list_users(self):
        "Проверка - Добавляет список участников в Event"
        ev1 = Event("event1", "event1_descr", "event1_own",
                    ["user1", "user2"], datetime(2007, 12, 6),
                    repeat_type='D', id='id1')
        ev1.add_list_users(['new_user1'])
        self.assertEqual(ev1._event_guests, ["user1", "user2", "new_user1"])

    def test_remove_list_users(self):
        "Удаляет список участников в Event"
        ev1 = Event("event1", "event1_descr", "event1_own",
                    ["user1", "user2","user3"], datetime(2007, 12, 6),
                    repeat_type='D', id='id1')
        ev1.remove_list_guests(['user3', 'user2'])
        self.assertEqual(ev1._event_guests, ["user1"])

    def test_str(self):
        "Проверка - Возвращает информацию для пользователя"
        ev1 = Event("event1", "event1_descr", "event1_own",
                    ["user1", "user2","user3"], datetime(2007, 12, 6),
                    repeat_type='D', id='id1')
        self.assertEqual(ev1.__str__(),f"Название события {ev1._name_event} с id {ev1._id}")

    def test_repr(self):
        "Проверка - Возвращает информацию для разработчика"
        ev1 = Event("event1", "event1_descr", "event1_own",
                    ["user1", "user2", "user3"], datetime(2007, 12, 6),
                    repeat_type='D', id='id1')
        self.assertEqual(ev1.__repr__(), f"[{ev1._id}:{ev1._name_event}]")


    def test_change_id_counter(self):
        'Проверка изменения счетчика'
        old_counter = Event.__id_counter__
        new_counter = 456
        Event.change_id_counter(new_counter)
        self.assertTrue(Event.__id_counter__ == new_counter)
        self.assertTrue(Event.__id_counter__ != old_counter)

    def test_repeat_events_Daily(self):
        "Проверка - Метод обработки повторения события ЕЖЕДНЕВНОГО"
        evd = Event("event1", "event1_descr", "event1_own",
                    ["user1", "user2"], datetime(2007, 12, 6),
                    repeat_type='D', id='id1')
        i = 0
        lst_result= []
        for elem in evd.repeat_events():
            i += 1
            if i >3:
                break
            lst_result.append(elem)
        lst_result = set(lst_result)
        check_result = set([datetime(2007, 12, 6),
                           datetime(2007, 12, 7),
                           datetime(2007, 12, 8)])
        self.assertSetEqual(lst_result,check_result)

    def test_repeat_events_Weekly(self):
        "Проверка - Метод обработки повторения события ЕЖЕНЕДЕЛЬНОГО"
        evd = Event("event1", "event1_descr", "event1_own",
                    ["user1", "user2"], datetime(2007, 12, 25),
                    repeat_type='W', id='id1')
        i = 0
        lst_result= []
        for elem in evd.repeat_events():
            i += 1
            if i >3:
                break
            lst_result.append(elem)
        lst_result = set(lst_result)
        check_result = set([datetime(2007, 12, 25),
                           datetime(2008, 1, 1),
                           datetime(2008, 1, 8)])
        self.assertSetEqual(lst_result,check_result)

    def test_repeat_events_Monthly(self):
        "Проверка - Метод обработки повторения события ЕЖЕМЕСЯЧНОГО"
        evd = Event("event1", "event1_descr", "event1_own",
                    ["user1", "user2"], datetime(2007, 12, 25),
                    repeat_type='M', id='id1')
        i = 0
        lst_result= []
        for elem in evd.repeat_events():
            i += 1
            if i >3:
                break
            lst_result.append(elem)
        lst_result = set(lst_result)
        check_result = set([datetime(2007, 12, 25),
                           datetime(2008, 1, 25),
                           datetime(2008, 2, 25)])
        self.assertSetEqual(lst_result,check_result)

    def test_repeat_events_Year(self):
        "Проверка - Метод обработки повторения события ЕЖЕГОДНОГО"
        evd = Event("event1", "event1_descr", "event1_own",
                    ["user1", "user2"], datetime(2007, 12, 25),
                    repeat_type='Y', id='id1')
        i = 0
        lst_result= []
        for elem in evd.repeat_events():
            i += 1
            if i > 3:
                break
            lst_result.append(elem)
        lst_result = set(lst_result)
        check_result = set([datetime(2007, 12, 25),
                           datetime(2008, 12, 25),
                           datetime(2009, 12, 25)])
        self.assertSetEqual(lst_result, check_result)

    def test_repeat_events_Once(self):
        "Проверка - Метод обработки повторения события ОДИНОЧНОГО"
        evd = Event("event1", "event1_descr", "event1_own",
                    ["user1", "user2"], datetime(2007, 12, 25),
                    repeat_type='N', id='id1')
        i = 0
        lst_result= []
        for elem in evd.repeat_events():
            i += 1
            if i > 3:
                break
            lst_result.append(elem)
        lst_result = set(lst_result)
        check_result = set([datetime(2007, 12, 25),
                           datetime(2007, 12, 25),
                           datetime(2007, 12, 25)])
        self.assertSetEqual(lst_result, check_result)

if __name__ == '__main__':
    unittest.main()

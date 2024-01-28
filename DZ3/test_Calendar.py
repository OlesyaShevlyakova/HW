import unittest
from Calendar import Calendar

class TestItem(unittest.TestCase):
    def test_init_calendar(self):
        "Проверка создания календаря - стандартно"
        cal1 = Calendar('iduser1','work')
        self.assertEqual(cal1._id_user, "iduser1")
        self.assertEqual(cal1._name_calendar, "work")

    def test_init_calendar_custom(self):
        "Проверка создания календаря - с доп.параметрами"
        cal1 = Calendar('iduser1','work',id=1, id_events=['id_evetn1', 'id_event2'])
        self.assertEqual(cal1._id_user, "iduser1")
        self.assertEqual(cal1._name_calendar, "work")
        self.assertEqual(cal1._id, '1')
        self.assertEqual(cal1._events, ['id_evetn1', 'id_event2'])

    def test_init_calendar_check_id_counter(self):
        "Проверка работы счетчика при создании нескольких календарей"
        id_counter_before_creating = Calendar.__id_counter__
        cal1 = Calendar('iduser1','work')
        cal2 = Calendar('iduser1','work')
        cal3 = Calendar('iduser1','work')
        cal4 = Calendar('iduser1','work')
        self.assertEqual(cal1._id, str(id_counter_before_creating))
        id_counter_before_creating += 1
        self.assertEqual(cal2._id, str(id_counter_before_creating))
        id_counter_before_creating += 1
        self.assertEqual(cal3._id, str(id_counter_before_creating))
        id_counter_before_creating += 1
        self.assertEqual(cal4._id, str(id_counter_before_creating))

    def test_change_id_counter(self):
        'Проверка изменения счетчика'
        old_counter = Calendar.__id_counter__
        new_counter = 456
        Calendar.change_id_counter(new_counter)
        self.assertTrue(Calendar.__id_counter__ == new_counter)
        self.assertTrue(Calendar.__id_counter__ != old_counter)

    def test_info_events(self):
        'Проверка отображения информации об ивентах календаря'
        cal1 = Calendar('iduser1','work', id_events=['id_evetn1', 'id_event2'])
        self.assertEqual(cal1.info_events(), ['id_evetn1', 'id_event2'])

    def test_info_id_user(self):
        'Проверка отображения информации об id пользователе'
        cal1 = Calendar('iduser1','work', id_events=['id_evetn1', 'id_event2'])
        self.assertEqual(cal1.info_id_user(), 'iduser1')

    def test_info_calendars(self):
        'Проверка возврата информации о календаре'
        cal1 = Calendar('iduser1','work', id_events=['id_evetn1', 'id_event2'],id=1)
        self.assertEqual(cal1.info_calendars(), ('1','work','iduser1',['id_evetn1', 'id_event2']))

    def test_change_name(self):
        'Проверка изменения имени календаря'
        cal1 = Calendar('iduser1','work', id_events=['id_evetn1', 'id_event2'],id=1)
        cal1.change_name('new_name')
        self.assertEqual('new_name', cal1._name_calendar)

    def test_add_event(self):
        'Проверка добавления событий в календарь'
        cal1 = Calendar('iduser1','work', id_events=['id_evetn1', 'id_event2'],id=1)
        event1 = 'id_event3'
        cal1.add_event(event1)
        self.assertEqual(cal1._events,['id_evetn1', 'id_event2', 'id_event3'])

    def test_delete_event(self):
        'Проверка удаления события из календаря'
        cal1 = Calendar('iduser1','work', id_events=['id_evetn1', 'id_event2'],id=1)
        cal1.delete_event('id_evetn1')
        self.assertEqual(cal1._events, ['id_event2'])

    def test_str(self):
        'Проверка __str__'
        cal1 = Calendar('iduser1','work', id_events=['id_evetn1', 'id_event2'],id=1)
        self.assertEqual(str(cal1),f"Календарь {cal1._id}, пользователя {cal1._id_user}")

    def test_repr(self):
        'Проверка __repr__'
        cal1 = Calendar('iduser1','work', id_events=['id_evetn1', 'id_event2'],id=1)
        self.assertEqual(cal1.__repr__(),f"[{cal1._id}:{cal1._id_user}]")


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

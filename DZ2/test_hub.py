from hub import Hub
from item import Item
from datetime import datetime
import unittest


class TestHub(unittest.TestCase):
    def test_hub_singleton(self):
        'Проверка того что hub - синглтон'  # небольшая документация к тесту
        my_hub = Hub()  # создаем первый объект класса
        his_hub = Hub()  # создаем второй объект класса
        self.assertTrue(my_hub is his_hub)

    def test_len(self):
        'Проверка того что при добавлении предметов меняется значение len(item)'
        h = Hub()
        h.items = []
        lst_name = ["карандаш", "ручка", "линейка", "маркер", "резинка"]
        lst_tags = ["мягкий", "синяя", "прозрачная", "черный", "с запахом"]
        for i in range(5):
            # h.add_item(Item()), ваш конструктор может отличаться, передайте нужные параметры
            h.add_item(Item(lst_name[i], tags=lst_tags[i]))
        self.assertEqual(len(h), 5)

    def test_getitem(self):
        'Проверка того, что по Hub можно итерироваться и брать i-тый элемент, используя [ i ]'
        h = Hub()
        h.items = []
        h.add_item(Item("pen", tags='blue'))
        h.add_item(Item("pensil", tags='white'))
        h.add_item(Item("book", tags='boring'))
        # если данный фрагмент кода не выполнится, то Hub не итерируется
        # КАК ДАННУЮ ПРОВЕРКУ РЕАЛИЗОВАТЬ НОРМАЛЬНО, ТО ЕСТЬ ЧЕРЕЗ ASSERT?
        # ЧТОБЫ ТЕСТ ПАДАЛ НЕ С ERROR, А С FAIL?
        for elem in h:
            pass
        self.assertEqual(h[1].name, 'pensil')

    def test_find_by_id1(self):
        'Проверка поиска по id'
        h = Hub()
        obj1 = Item()
        obj2 = Item()
        obj3 = Item()
        obj1_id = obj1._id
        h.add_item(obj1)
        h.add_item(obj2)
        h.add_item(obj3)
        self.assertTupleEqual(h.find_by_id(obj1_id), (0, obj1))

    def test_find_by_id2(self):
        'Проверка поиска по несуществующему id'
        h = Hub()
        obj_id = 123
        self.assertTupleEqual(h.find_by_id(obj_id), (-1, None))

    def test_find_by_tags(self):
        'Проверка возврата контейнера, который содержит все предметы из items, у которого есть ВСЕ теги из tags'
        h = Hub()
        obj1 = Item(name="pen", tags=['red', 'plastic', 'white'])
        obj2 = Item(name="pensil", tags=['blue', 'plastic', 'white'])
        obj3 = Item(name="book", tags=['boring'])
        h.add_item(obj1)
        h.add_item(obj2)
        h.add_item(obj3)
        find_tags = ['plastic', 'white']
        self.assertEqual(h.find_by_tags(find_tags), [obj1, obj2])

    def test_rm_item(self):
        "Проверка удаления item с id=elem или удаления item=elem"
        h = Hub()
        obj1 = Item()
        obj2 = Item()
        obj3 = Item()
        h.add_item(obj1)
        h.add_item(obj2)
        obj1_id = obj1._id
        h.rm_item(obj1_id)
        self.assertTupleEqual(h.find_by_id(obj1_id), (-1, None))
        h.rm_item(obj2)
        self.assertFalse(obj2 in h.items)
        self.assertEqual(h.rm_item(obj3), None)

    def test_drop_items(self):
        "Проверка удаления всех товаров из Hub, которые содержатся в items"
        h = Hub()
        obj4 = Item()
        obj5 = Item()
        obj6 = Item()
        h.add_item(obj4)
        h.add_item(obj5)
        h.add_item(obj6)
        h.drop_items([obj4, obj5])
        self.assertFalse([obj4, obj5] in h.items)
        h.items.clear()

    def test_clear(self):
        "Проверка очищения всего контейнера items"
        h = Hub()
        obj4 = Item()
        obj5 = Item()
        obj6 = Item()
        h.add_item(obj4)
        h.add_item(obj5)
        h.add_item(obj6)
        self.assertEqual(h.clear(), None)
        h.items.clear()

    def test_date(self):
        "Проверка установки даты в хабе"
        h = Hub()
        self.assertEqual(h.date, h._date)
        date_now = datetime.now()
        h.date = date_now
        self.assertEqual(date_now, h._date)

    def test_find_by_date(self):
        "Проверка возвращения листа всех Item, подходящих по дате"
        h = Hub()
        h.items.clear()
        obj1 = Item(dispatch_time=datetime(2020, 12, 25))
        obj2 = Item(dispatch_time=datetime(2021, 5, 8))
        obj3 = Item(dispatch_time=datetime(2023, 10, 9))
        h.add_item(obj1)
        h.add_item(obj2)
        h.add_item(obj3)
        new_date1 = datetime(2021, 5, 8)
        new_date2 = datetime(2025, 10, 9)
        new_date3 = datetime(2018, 10, 9)
        self.assertEqual(h.find_by_date(new_date1), [obj1, obj2])
        self.assertEqual(h.find_by_date(new_date1, new_date2), [obj2, obj3])
        self.assertRaises(Exception, h.find_by_date(new_date3))
        h.items.clear()

    def test_add_item(self):
        "Проверка добавления нового items в Hub (типо Item или его наследника)"
        h = Hub()
        h.items.clear()
        obj1 = Item()
        obj2 = Item()
        obj3 = Item()
        obj4 = 123
        h.add_item(obj1)
        h.add_item(obj2)
        h.add_item(obj3)
        h.add_item(obj4)
        self.assertEqual(len(h), 3)

    def test_find_most_valuable(self, amount=1):
        "Проверка возвращения первых amount самых дорогих предметов на складе или всех"
        h = Hub()
        h.items.clear()
        obj1 = Item(cost=1000)
        obj2 = Item(cost=500)
        obj3 = Item(cost=100)
        h.add_item(obj1)
        h.add_item(obj2)
        h.add_item(obj3)
        list_obj1 = h.find_most_valuable(5)
        list_obj2 = h.find_most_valuable(2)
        list_obj4 = h.find_most_valuable(1)
        self.assertEqual(len(list_obj1), 3)
        self.assertEqual(len(list_obj2), 2)
        self.assertEqual(h.find_most_valuable(2), [obj1, obj2])
        h.items.clear()
        list_obj3 = h.find_most_valuable(2)
        self.assertEqual(len(list_obj3), 0)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)



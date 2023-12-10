import unittest
from item import Item

class TestItem(unittest.TestCase):
    def test_item_id(self):
        'Проверка того, что у разных Items разные id'
        pen1 = Item()
        pen2 = Item()
        self.assertTrue(pen1._id is not pen2._id)

    def test_len(self):
        'Проверка того, что при добавлении тэгов меняется значение len(item)'
        # Реализуйте проверку того что при добавлении тэгов меняется значение len(item)
        # print('1 - ',h.tags)
        h = Item()
        lst_tags = ["мягкий", "синяя", "прозрачная", "черный", "с запахом"]
        for i in range(5):
            h.add_tag(lst_tags[i])
        self.assertEqual(len(h), 5)

    def test_equal_tags(self):
        'Проверка того, что если к предмету добавить два идентичных тега - их количество будет один'
        # Реализуйте проверку того что если к предмету добавить два идентичных тега - их колчество будет один
        h1 = Item()
        h1.add_tag("пластик")
        h1.add_tag("пластик")
        self.assertEqual(len(h1), 1)

    def test_set_cost(self):
        'Проверка того, что присваивается новая цена'
        h1 = Item(cost=1500)
        new_cost = 1000
        h1.set_cost(new_cost)
        self.assertEqual(h1._cost, new_cost)

    def test_get_cost(self):
        'Проверка того, что выводится цена'
        h1 = Item(cost=1500)
        self.assertEqual(h1.get_cost(), 1500)

    def test_lt_(self):
        'Проверка того, что больший объект тот, у которого большая цена'
        h1 = Item(cost=1500)
        h2 = Item(cost=2000)
        self.assertTrue(h2 > h1)
        self.assertFalse(h1 > h2)
        self.assertFalse(h1 == h2)

    def test_add_tags(self):
        'Проверка того, что можно добавлять несколько tags'
        h1 = Item(tags=["blue", "yellow"])
        h1.add_tags("plastic", 'slim')
        self.assertEqual(h1.tags, ["blue", "yellow"] + ["plastic", 'slim'])

    def test_rm_tags(self, *tags):
        'Проверка того, что можно удалять несколько tags'
        h1 = Item(tags=["blue", "yellow", "plastic", 'slim'])
        h1.rm_tags("plastic", 'slim')
        self.assertEqual(h1.tags, ["blue", "yellow"])

    def test_is_tagged(self):
        "Проверка на проверку, что введенные tags присутствуют в tags объекта"
        h1 = Item(tags=["blue", "yellow", "plastic", 'slim'])
        self.assertTrue(h1.is_tagged("blue", "yellow"))
        self.assertFalse(h1.is_tagged("red", "white"))

    def test_copy(self):
        "Проверка, что создается копия существующего объекта, но с другим id"
        test_item1 = Item(name="pen", discryption="blue", cost=1000)
        test_item2 = test_item1.copy()
        self.assertTrue(test_item1.name == test_item2.name and test_item1.discryption == test_item2.discryption and test_item1._cost == test_item2._cost)
        self.assertFalse(test_item1._id == test_item2._id)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

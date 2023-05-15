import unittest

from azbaseliner.util.collections import ListUtils, DictUtils


class TestListUtils(unittest.TestCase):
    def test_001_ckunking_under_size(self) -> None:
        items: list = [1, 2, 3, 4, 5, 6, 7]
        maxSize = 20
        itemLists = ListUtils.splitIntoChunks(items, maxSize)
        self.assertEqual(len(itemLists), 1)

    def test_002_ckunking_over_size(self) -> None:
        items: list = [1, 2, 3, 4, 5, 6, 7]
        maxSize = 2
        itemLists = ListUtils.splitIntoChunks(items, maxSize)
        self.assertEqual(len(itemLists), 4)


class TestDictUtils(unittest.TestCase):
    def test_001_simple_dict_merge(self) -> None:
        a: dict = {"a": 10, "b": 10}
        b: dict = {"c": 10, "d": 10}
        c: dict = DictUtils.mergeDicts(a, b)
        self.assertEqual(c["a"], 10)
        self.assertEqual(c["b"], 10)
        self.assertEqual(c["c"], 10)
        self.assertEqual(c["d"], 10)

    def test_002_item_dict_merge(self) -> None:
        a: dict = {"a": [10, 11], "b": 10}
        b: dict = {"a": [12], "d": 10}
        c: dict = DictUtils.mergeDicts(a, b)
        self.assertTrue(10 in c["a"])
        self.assertTrue(11 in c["a"])
        self.assertTrue(12 in c["a"])

    def test_003_item_dict_nested_merge(self) -> None:
        a: dict = {"a": {"x": [10], "y": [11]}, "b": {"y": [42, 17]}}
        b: dict = {"a": {"x": [11], "y": [12]}}
        c: dict = DictUtils.mergeDicts(a, b)
        self.assertTrue(10 in c["a"]["x"])
        self.assertTrue(11 in c["a"]["x"])
        self.assertTrue(11 in c["a"]["y"])
        self.assertTrue(12 in c["a"]["y"])
        self.assertTrue(42 in c["b"]["y"])
        self.assertTrue(17 in c["b"]["y"])
        self.assertEqual(len(c.keys()), 2)

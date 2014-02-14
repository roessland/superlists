from django.core.exceptions import ValidationError
from django.test import TestCase
from ..models import Item, List


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List.objects.create()

        first_item = Item.objects.create(text="The first (ever) list item", list=list_)
        second_item = Item.objects.create(text="Item the second", list=list_)

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, "Item the second")
        self.assertEqual(first_saved_item.list, list_)

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/%d/' % (list_.id))

    def test_cannot_save_duplicate_items(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text="blabla")
        with self.assertRaises(ValidationError):
            Item.objects.create(list=list_, text="blabla")

    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text="bla")
        Item.objects.create(list=list2, text="bla") # Should not raise error

    def test_list_ordering(self):
        list_ = List.objects.create()
        item1 = Item.objects.create(list=list_, text="i1")
        item2 = Item.objects.create(list=list_, text="item 2")
        item3 = Item.objects.create(list=list_, text="3")
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_string_representation(self):
        list_ = List.objects.create()
        item = Item.objects.create(list=list_, text="some text")
        self.assertEqual(str(item), item.text)

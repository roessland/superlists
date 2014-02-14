from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.utils.html import escape
from ..models import Item, List
from ..views import home_page
from ..forms import ItemForm, EMPTY_LIST_ERROR
import unittest

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_input_means_nothing_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(List.objects.count(), 0)


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        response = self.client.post(
            '/lists/new',
            data={'text': "A new list item"}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'text': "A new list item"}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_validation_errors_end_up_on_home_page(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_LIST_ERROR))

    def test_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)



class ListViewTest(TestCase):

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text="Itemey 1", list=correct_list)
        Item.objects.create(text="Itemey 2", list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text="Other list item 1", list=other_list)
        Item.objects.create(text="Other list item 2", list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, "Itemey 1")
        self.assertContains(response, "Itemey 2")
        self.assertNotContains(response, "Other list item 1")
        self.assertNotContains(response, "Other list item 2")

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data={'text': "A new item for an existing list"}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data={'text': "A new item for an existing list"}
        )

        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))

    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(
            '/lists/%d/' % (list_.id,),
            data={'text': ''}
        )
        self.assertTemplateUsed(response, 'lists/list.html')
        expected_error = escape(EMPTY_LIST_ERROR)
        self.assertContains(response, expected_error)

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')

    def test_form_save_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'testlol'})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'testlol')
        self.assertEqual(new_item.list, list_)

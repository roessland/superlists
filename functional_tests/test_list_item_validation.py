from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home pages and accidentally submits an empty list
        # item.
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('new-item').send_keys("\n")

        # The home page refreshes, and there is an error message saying that
        # list items cannot be blank
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # She tries again with some text for the item, which now works
        self.browser.find_element_by_id('new-item').send_keys("Buy milk\n")
        self.check_for_row_in_list_table('1: Buy milk')

        # She submits a seconds blank list item
        self.browser.find_element_by_id('new-item').send_keys("\n")

        # She receives a similar warning on the list page, and the first item
        # still exists
        self.check_for_row_in_list_table('1: Buy milk')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # And she can correct it by filling some text in
        self.browser.find_element_by_id('new-item').send_keys("Make tea")
        self.check_for_row_in_list_table("1: Buy milk")
        self.check_for_row_in_list_table("2: Make tea")

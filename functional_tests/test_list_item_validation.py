from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home pages and accidentally submits an empty list
        # item.

        # The home page refreshes, and there is an error message saying that
        # list items cannot be blank

        # She tries again with some text for the item, which now works

        # She submits a seconds blank list item

        # She receives a similar warning on the list page

        # And she can correct it by filling some text in
        self.fail("Write me!")

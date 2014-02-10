import sys
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if "liveserver" in arg:
                cls.server_url = "http://" + arg.split('=')[1]
                return
        LiveServerTestCase.setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            LiveServerTestCase.tearDownClass()

    def setUp(self):
        self.browser = webdriver.PhantomJS()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('list-table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith visits the front page
        self.browser.get(self.server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('new-item')
        self.assertEqual(inputbox.get_attribute('placeholder'), "Enter a to-do item")

        # She types "Buy peacock feathers" into a text box and presses enter.
        # The pages updates to a new URL, and she can see "1: Buy peacock
        # feathers" as an item in a to-do list table
        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table("1: Buy peacock feathers")

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id('new-item')
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table("1: Buy peacock feathers")
        self.check_for_row_in_list_table("2: Use peacock feathers to make a fly")

        # Now a new user, Francis comes along to the site

        ## Open a new browser session to make sure Edith's session is gone
        self.browser.quit()
        self.browser = webdriver.PhantomJS()

        # Francis visits the home page. There is no sign of Edith's list
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)

        # Francis starts a new list by entering a new item
        inputbox = self.browser.find_element_by_id("new-item")
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)

        # Francis gets his how unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trance of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)

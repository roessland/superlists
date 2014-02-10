from .base import FunctionalTest


class StaticFilesTest(FunctionalTest):

    def test_static_image_file_available(self):
        # Edith goes directly to an URL containing her favourite image
        self.browser.get(self.server_url + '/static/pink_mascot.jpg')

        # She sees that an image is visible in the browser, and it has the same
        # size as her favourite image
        img = self.browser.find_element_by_tag_name('img')
        self.assertEqual(img.size['height'], 200)
        self.assertEqual(img.size['width'], 400)

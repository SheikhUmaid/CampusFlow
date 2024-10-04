from django.test import TestCase

# Create your tests here.


# create a test case for the index page


class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/landing_page.html')
        self.assertContains(response, 'CampusFlow')
        # self.assertContains(response, 'Home')
        # self.assertContains(response, 'About')
        # self.assertContains(response, 'Contact')
        self.assertContains(response, 'register')
        self.assertContains(response, 'login')
        self.assertContains(response, ' SDM CampusFlow')
        
# how to run these tests?
# python manage.py test

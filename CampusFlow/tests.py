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


class LoginPageTestCase(TestCase):
    def test_login_page(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/login.html')
        self.assertContains(response, 'Login')
        self.assertContains(response, 'Username')
        self.assertContains(response, 'Password')
        self.assertContains(response, 'Register')
        self.assertContains(response, 'Forgot Password?')
        self.assertContains(response, 'Sign in')
        self.assertContains(response, 'SDM CampusFlow')
        
        


class RegisterPageTestCase(TestCase):
    def test_register_page(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/register.html')
        self.assertContains(response, 'Register')
        self.assertContains(response, 'Username')
        self.assertContains(response, 'Email')
        self.assertContains(response, 'Password')
        self.assertContains(response, 'Confirm Password')
        self.assertContains(response, 'Already have an account?')
        self.assertContains(response, 'Login')
        self.assertContains(response, 'SDM CampusFlow')
        
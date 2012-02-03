from django.core import mail
from django.test import Client, TestCase

from red.managers import TradeManager

class ViewTestCase(TestCase):
    """Helper class for testing URLs."""
    fixtures = ['test.json']

    def setUp(self):
        self.client = Client()
        self.url_prefix = '/red'
    
    def create_urls(self, urls):
        return ['/'.join([self.url_prefix, url]) for url in urls]

    def test_create_urls_correct(self):
        urls = ['', 'about/', 'contact']
        created_urls = self.create_urls(urls)
        # same number of elements
        self.assertEqual(len(urls), len(created_urls))
        # with the url prefix for the application
        original_and_created_urls = zip(urls, created_urls)
        for original, created in original_and_created_urls:
            self.assertEqual(self.url_prefix + '/' + original, created)

    def assertHTTPOk(self, url):
        """Checks that the given URL returns a 200 HTTP code."""
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def assertTemplatesUsed(self, response, templates):
        """
        Checks that every template in ``template`` was rendered 
        in ``response``.
        """
        for template in templates:
            self.assertTemplateUsed(response, template)


class TestIndex(ViewTestCase):
    """Index page."""
    def setUp(self):
        ViewTestCase.setUp(self)
        self.trades = TradeManager()
        self.urls = self.create_urls([''])
        self.templates = ['base.html', 'index.html',]
        if len(self.trades.latest()):
            self.templates.append('includes/trade.html')

    def test_index_http_ok(self):
        for url in self.urls:
            self.assertHTTPOk(url)

    def test_templates(self):
        for url in self.urls:
            response = self.client.get(url)
            self.assertTemplatesUsed(response, self.templates)


class TestAbout(ViewTestCase):
    """About page."""
    def setUp(self):
        ViewTestCase.setUp(self)
        self.urls = self.create_urls(['about', 'about/'])
        self.templates = ['base.html', 'about.html']

    def test_about_http_ok(self):
        for url in self.urls:
            self.assertHTTPOk(url)

    def test_templates(self):
        for url in self.urls:
            response = self.client.get(url)
            self.assertTemplatesUsed(response, self.templates)


class TestContact(ViewTestCase):
    """Contact page."""
    def setUp(self):
        ViewTestCase.setUp(self)
        self.urls = self.create_urls(['contact', 'contact/'])
        self.templates = ['base.html', 'contact.html', 'includes/form.html']

    def test_about_http_ok(self):
        for url in self.urls:
            self.assertHTTPOk(url)

    def test_templates(self):
        for url in self.urls:
            response = self.client.get(url)
            self.assertTemplatesUsed(response, self.templates)

    def test_invalid_contact_form_post_templates(self):
        # when an invalid form is submitted, the contact page 
        # is rendered again
        form = {'subject': 'test',
                'message': 'test message',
                'sender': 'invalidemail',
                'cc_myself': True}
        for url in self.urls:
            response = self.client.post(url, form)
            self.assertTemplatesUsed(response, self.templates)

    def test_valid_contact_form_post_templates(self):
        # when a valid form is submitted, redirect to "thank you" page
        form = {'subject': 'test',
                'message': 'test message',
                'sender': 'validemail@foo.bar',
                'cc_myself': True}
        templates = ['base.html', 'thankyou.html']
        for url in self.urls:
            response = self.client.post(url, form)
            self.assertTemplatesUsed(response, templates)

    def test_mail_to_admins_with_valid_contact_form_post(self):
        # without self CC
        form = {'subject': 'test',
                'message': 'test message',
                'sender': 'validemail@foo.bar',
                'cc_myself': False}
        for url in self.urls:
            self.client.post(url, form)
            self.assertEqual(1, len(mail.outbox))
            mail.outbox = []

    def test_mail_to_admins_and_user_with_valid_contact_form_post(self):
        # with self CC
        form = {'subject': 'test',
                'message': 'test message',
                'sender': 'validemail@foo.bar',
                'cc_myself': True}
        for url in self.urls:
            self.client.post(url, form)
            self.assertEqual(1, len(mail.outbox))
            mail.outbox = []

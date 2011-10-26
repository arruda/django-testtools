# coding:utf-8
from django.core.urlresolvers import reverse, NoReverseMatch
from django import test
from django.test.client import Client
from django.conf import settings


class ReverserClient(Client):

    def _resolve(self, path, kwargs):
        """
        Helper method to enable automatic resolution of named urls.

        def test_method(self):
            self.get('namespace:name', args=[1])
            self.get('/hardcoded/url/')
            self.post('namespace:name', args=[2], data={'key': value})
            self.post(('namespace:name', [2]), {'key': value})
            self.post('namespace:name', {'key': value}, args=[2])
            self.post('/hardcoded/url/', {'key': value})

        """
        # If path is a tuple, pass it right to reverse
        if isinstance(path, (tuple, list)):
            return reverse(path)

        # extract reverse's args if present in kwargs.
        args = kwargs.pop('args', [])

        try:
            return reverse(path, args=args)
        except NoReverseMatch:
            return path

    def get(self, path, *args, **kwargs):
        resolved_path = self._resolve(path, kwargs)
        return super(ReverserClient, self).get(resolved_path, *args, **kwargs)

    def post(self, path, *args, **kwargs):
        resolved_path = self._resolve(path, kwargs)
        return super(ReverserClient, self).post(resolved_path, *args, **kwargs)

class TestCase(test.TestCase):
    client_class = ReverserClient

    def __clean_template_output(self, response):
        splited_content = response.content.strip().splitlines()
        wrong_lines = [i for i, line in enumerate(splited_content) if settings.TEMPLATE_STRING_IF_INVALID in line]

        #Condição para não executar código "de graça" no caso do assert
        # não falhar
        if wrong_lines:
            html_errors = ''
            for error_line in wrong_lines:
                html_errors += '\n'.join(splited_content[error_line-2:error_line+3])
                html_errors += '\n##############################################\n'

            template_names = '\n\t'.join([t.name.encode('utf-8') for t in response.template])
            error_message = 'Variáveis inválidas no(s) template(s)\n\t%s ' % template_names
            error_message += '\nTrechos de html com erro:\n%s'% html_errors

            return error_message

    def assertTemplateUsed(self, response, template_name):
        super(TestCase, self).assertTemplateUsed(response, template_name)
        self.longMessage = False
        self.assertIn('MEDIA_URL', response.context)
        self.assertEqual(response.context['MEDIA_URL'], settings.MEDIA_URL)
        self.assertIn('STATIC_URL', response.context)
        self.assertEqual(response.context['STATIC_URL'], settings.STATIC_URL)
        self.assertNotIn(settings.TEMPLATE_STRING_IF_INVALID, response.content, self.__clean_template_output(response))

    def assertErrorsInForm(self, form, *args, **kwargs):
        """
        Assert that form only has *args errors.
        If validate=True, call form.is_valid()
        """
        if kwargs.get('validate', False):
            self.assertFalse(form.is_valid())
        for field in args:
            self.assertIn(field, form.errors)
        self.assertEqual(len(form.errors), len(args))

    def assertQuerySetEqual(self, qs1, qs2, *args, **kwargs):
        self.assertEqual(list(qs1), list(qs2), *args, **kwargs)

    def assertRecipients(self, email, recipients):
        email_recipients = email.recipients()
        self.assertEqual(len(email_recipients), len(recipients))
        for r in recipients:
            self.assertIn(r, email_recipients)

# coding:utf-8
from django import test
from django.conf import settings

from client import ReverserClient

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

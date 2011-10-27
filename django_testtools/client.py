# coding:utf-8
from django.core.urlresolvers import reverse, NoReverseMatch
from django.test.client import Client

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

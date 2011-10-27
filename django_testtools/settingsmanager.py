# coding:utf-8
# http://djangosnippets.org/snippets/1011/
from django.conf import settings
from django.core.urlresolvers import set_urlconf
from django.core.management import call_command
from django.db.models import loading
from django.test import TestCase

NO_SETTING = ('!', None)

def postset_installed_apps():
    from django.utils.datastructures import SortedDict
    loading.cache.loaded = False
    # For some reason south needs these values to be reset
    if 'south' in settings.INSTALLED_APPS:
        loading.cache.app_store = SortedDict()
        loading.cache.app_models = SortedDict()
    call_command('syncdb', verbosity=0)

def postset_root_urlconf():
    from django.core.urlresolvers import clear_url_caches
    clear_url_caches()

def postset_template_context_processors():
    # Force re-evaluation of the contex processor list
    import django.template.context
    django.template.context._standard_context_processors = None


class TestSettingsManager(object):
    """
    A class which can modify some Django settings temporarily for a
    test and then revert them to their original values later.

    Automatically handles resyncing the DB if INSTALLED_APPS is
    modified.

    """
    def __init__(self):
        self._original_settings = {}

    def push(self, name, value):
        # save original value
        self._original_settings.setdefault(name, getattr(settings, name, NO_SETTING))

        if name == 'ROOT_URLCONF':
            set_urlconf(value)
        else:
            setattr(settings, name, value)

    def pop(self, name):
        value = self._original_settings.get(name)

        if not value:
            return

        if value == NO_SETTING:
            delattr(settings, name)
        else:
            # special case
            if name == 'ROOT_URLCONF':
                set_urlconf(value)
            else:
                setattr(settings, name, value)

    def clear_cache(self):
        caches = {
            'ROOT_URLCONF': postset_root_urlconf,
            'INSTALLED_APPS': postset_installed_apps,
            'TEMPLATE_CONTEXT_PROCESSORS': postset_template_context_processors
        }

        for name, invalidate in caches.iteritems():
            if name in self._original_settings:
                invalidate()

    def set(self, **kwargs):
        for k,v in kwargs.iteritems():
            self.push(k, v)

        self.clear_cache()

    def revert(self):
        for k,v in self._original_settings.iteritems():
            self.pop(k)
        self.clear_cache()
        self._original_settings = {}

    def filter(self, key, content):
        value = filter(lambda s: not s.endswith(content),
                       getattr(settings, key))
        self.set(**{ key: value })

    def append(self, key, content):
        value = list(set(list(getattr(settings, key, list())) + [content]))
        self.set(**{ key: value })

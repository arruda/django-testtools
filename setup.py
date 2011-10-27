from setuptools import setup

setup(
    name='django-testtools',
    version='0.1',
    author='Bernardo Fontes',
    author_email='falecomigo@bernardofontes.net',
    url='http://github.com/dekode/django-testtools',

    packages=['django_testtools'],
    install_requires=['setuptools', 'django'],
    license='http://www.gnu.org/licenses/lgpl.html',
    keywords='django testing',
    description="A helper for writting Django's tests",
)

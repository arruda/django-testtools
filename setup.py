from setuptools import setup

setup(
    name='django-testtools',
    version='0.1',
    author='Dekode',
    author_email='contato@dekode.com.br',
    url='http://github.com/dekode/django-testtools',

    packages=['src'],
    install_requires=['setuptools', 'django'],
    license='http://www.gnu.org/licenses/lgpl.html',
    keywords='django testing',
    description="A helper for writting Django's tests",
)

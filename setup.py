import os
from setuptools import setup, find_packages
import userextensions

with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as readme:
    README = readme.read()


with open('requirements.txt') as f:
    required = f.read().splitlines()

version = userextensions.__version__

setup(
    name='django-userextensions',
    description='A user extension module for django',
    long_description=README,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    version=version,
    license=userextensions.__license__,
    author=userextensions.__author__,
    author_email=userextensions.__email__,
    url='https://github.com/davidslusser/django-userextensions',
    download_url='https://github.com/davidslusser/django-userextensions/archive/{}.tar.gz'.format(version),
    keywords=['django', 'helpers', 'extension', 'user', 'profile'],
    install_requires=required,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Framework :: Django :: 4.2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

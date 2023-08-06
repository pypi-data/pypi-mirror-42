from os import path

from setuptools import setup, find_packages

with open(path.join(path.abspath(path.dirname(__file__)), 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='quickauth',
    version='0.2.21',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/valency/quickauth/',
    author='Ye Ding',
    author_email='guiewy@gmail.com',
    description='QuickAuth: A Quick User-Password Authentication for Python',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    keywords=['auth', 'authentication'],
    install_requires=[
        'redislite'
    ]
)

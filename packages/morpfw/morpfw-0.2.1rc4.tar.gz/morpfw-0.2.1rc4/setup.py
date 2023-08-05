from setuptools import setup, find_packages
import sys
import os

version = '0.2.1rc4'

long_description = open(
    os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(name='morpfw',
      version=version,
      description="Web framework based on morepath",
      long_description=long_description,
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Izhar Firdaus',
      author_email='izhar@kagesenshi.org',
      url='http://github.com/morpframework/morpfw',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'rulez>=0.1.2,<0.2.0',
          'more.cors',
          'celery',
          'redis',
          'jsl',
          'pyyaml>=4.2b1',
          'more.jsonschema',
          'jsonobject==0.9.4',
          'sqlalchemy',
          'more.signals',
          'DateTime',
          'transitions',
          'jsonpath_ng',
          'python-dateutil',
          'more.jwtauth',
          'more.itsdangerous',
          'sqlsoup',
          'celery',
          'gunicorn',
          'itsdangerous',
          'pyyaml',
          'passlib',
          'jsonschema',
          'more.transaction',
          'zope.sqlalchemy',
          'python-dateutil',
          'more.cors',
          'sqlalchemy_jsonfield',
          'sqlsoup',
          'celery',
          'gunicorn',
          'itsdangerous',
          'pyyaml',
          'passlib',
          'jsonschema',
          'more.transaction',
          'zope.sqlalchemy',
          'more.basicauth',
          'cryptography',
          'elasticsearch>=5.0.0,<6.0.0',
          'pamela',
          'click',
          'cookiecutter'
      ],
      extras_require={
          'test': [
              'nose',
              'webtest',
              'pytest==3.10.1',
              'pytest-html',
              'pytest_postgresql',
              'pytest_rabbitmq',
              'pytest-annotate',
              'pytest-cov',
              'pika',
          ]
      },
      entry_points={
          'morepath': ['scan=morpfw'],
          'console_scripts': [
              'morpfw=morpfw.cli:cli',
          ]
      }
      )

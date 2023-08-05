from setuptools import setup

setup(name='python-donodoo',
      version='0.1.0',
      description='Donodoo API Client',
      url='https://bitbucket.org/metadonors/python-donodoo',
      author='Metadonors',
      author_email='fabrizio.arzeni@metadonors.it',
      license='MIT',
      packages=['pydonodoo'],
      install_requires=[
          'OdooRPC',
      ],
      zip_safe=False)
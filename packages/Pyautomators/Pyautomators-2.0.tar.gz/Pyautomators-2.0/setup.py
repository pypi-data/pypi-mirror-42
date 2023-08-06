# -*- coding: utf-8 -*-
from setuptools import setup,find_packages

setup(name='Pyautomators',
      version='2.0',
      url='',
      license='Indra Company',
      author='Kaue Bonfim',
      author_email='koliveirab@indracompany.com',
      description='Automation library for complete generation of testicle environment',
      packages=['Pyautomators',
                  'Pyautomators.compat',
                  'Pyautomators.contrib',
                  'Pyautomators.formatter',
      			  'Pyautomators.reporter',
      			  ],
	  install_requires=['parse-type', 'six', 'parse'],
      zip_safe=True)
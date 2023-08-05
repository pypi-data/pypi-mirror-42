# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def get_version_from_file():
    # get version number from __init__ file
    # before module is installed

    fname = 'nadaprafazer/__init__.py'
    with open(fname) as f:
        fcontent = f.readlines()
    version_line = [l for l in fcontent if 'VERSION' in l][0]
    return version_line.split('=')[1].strip().strip("'").strip('"')


def get_long_description_from_file():
    # content of README will be the long description

    # fname = 'README'
    # with open(fname) as f:
    #     fcontent = f.read()
    # return fcontent
    return ''

VERSION = get_version_from_file()

DESCRIPTION = """
Simple crawler to list top reddit threads. Includes webhook stuff
for telegram bots!
""".strip()

LONG_DESCRIPTION = get_long_description_from_file()

setup(name='nadaprafazer',
      version=VERSION,
      author='Juca Crispim',
      author_email='juca@poraodojuca.net',
      url='https://github.com/jucacrispim/desafios/crawlers',
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      packages=find_packages(exclude=['tests', 'tests.*']),
      license='GPL',
      include_package_data=True,
      install_requires=['aiohttp', 'beautifulsoup4', 'sanic',
                        'async-dns', 'cchardet'],
      entry_points={
          'console_scripts':[
              'nadaprafazer=nadaprafazer.cli:main',
              'nadaprafazer-tgwebhook=nadaprafazer.web:main'
          ]
      },
      test_suite='tests',
      provides=['nadaprafazer'],)

#!/usr/bin/env python

from setuptools import setup, find_packages
import time

from recipe_scrapers import settings

def get_version():
    return "%s.%d" % (settings.VERSION, int(time.time()))

setup(
    name='recipe-scrapers',
    version=get_version(),
    description='Scrapes popular recipe sources and inserts them into a database',
    long_description='Scrapes popular recipe sources and inserts them into a database',
    author='Matt Jackson',
    author_email='me@mattjackson.eu',
    url='http://mattjackson.eu',
    packages=find_packages(),
    install_requires=['lxml', 'pymongo', 'argparse'],
    entry_points={
        'console_scripts': [
            'foodcom-scraper = allergy_assistant.scrapers.sites.foodcom:main',
            'bbcgoodfood-scraper = allergy_assistant.scrapers.sites.bbcgoodfood:main',
            'allrecipes-scraper = allergy_assistant.scrapers.sites.allrecipes:main',
            'foodnetwork-scraper = allergy_assistant.scrapers.sites.foodnetwork:main',
            'epicurious-scraper = allergy_assistant.scrapers.sites.epicurious:main',
            'foodchannel-scraper = allergy_assistnt.scrapers.sites.foodchannel:main',
            'reprocess-recipes = allergy_assistant.utils.reprocess_recipes:run',
        ]
    },
    classifiers=[
          'Environment :: Console',
          'Operating System :: Unix',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
    ],
)

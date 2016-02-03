#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='slack-emoji-search',
    version='0.0.1',
    description='Search across Slack for messages with a specific emoji.',
    author='Micah Saul',
    author_email='Micah.Saul@gsa.gov',
    url='https://github.com/18F/emoji_search',
    license='CC0 1.0 Universal',
    py_modules=['emoji_search'],
    install_requires=[
        "click",
        "requests",
    ],
    entry_points={
        'console_scripts': [
            'emoji_search = emoji_search:get_messages',
        ],
    },
)

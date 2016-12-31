from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='desugreet',

    version='1.1.0',

    description="a small discord-bot that greets new Members",
    long_description="a small discord-bot that greets new Members",

    url='https://github.com/AlexFence/DesuGreet',

    author='Alex Fence',
    author_email='alexfence.code@gmail.com',

    license='GPL',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='discord bot',

    packages=find_packages(),

    install_requires=['discord.py', 'dateutils'],
    entry_points={
      'console_scripts': [
          'desugreet = desugreet.__main__:main'
      ]
    },
)

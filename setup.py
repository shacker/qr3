#!/usr/bin/env python

from setuptools import setup, find_packages

version = '1.0.0'

LONG_DESCRIPTION = '''

Full documentation (with example code) is at http://github.com/doctorondemand/qr3

QR3
=====

**QR3** helps you create and work with **queue, capped collection (bounded queue),
deque, and stack** data structures for **Redis**. Redis is well-suited for
implementations of these abstract data structures, and QR3 makes it even easier to
work with the structures in Python.

Quick Setup
------------
You'll need [Redis](http://github.com/antirez/redis/ "Redis") itself (QR makes use 
of MULTI/EXEC, so you'll need the Git edge version), and the current Python interface
for Redis, [redis-py](http://github.com/andymccurdy/redis-py "redis-py"). 

Run setup.py to install qr3 or 'pip install qr3'.

'''

setup(
    name                 = 'qr3',
    version              = version,
    description          = 'Redis-powered queues, capped collections, deques, and stacks',
    long_description     = LONG_DESCRIPTION,
    url                  = 'http://github.com/doctorondemand/qr3',
    author               = 'Ted Nyman',
    author_email         = 'ted@ted.io',
    maintainer           = 'DoctorOnDemand',
    maintainer_email     = 'dev@doctorondemand.com',
    keywords             = 'Redis, queue, data structures',
    license              = 'MIT',
    packages             = find_packages(),
    install_requires     = ['future', 'redis'],
    py_modules           = ['qr'],
    include_package_data = True,
    zip_safe             = False,
    classifiers          = [
	    'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
   ],
)

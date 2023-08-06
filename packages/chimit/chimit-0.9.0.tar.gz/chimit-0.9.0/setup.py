from __future__ import print_function

import os
import sys

from setuptools import setup

# sys.path.insert(0, '.')
import chimit # pylint: disable=wrong-import-position

read_md = lambda f: open(f, 'r').read()

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


def read(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, 'rb') as fin:
        text = fin.read().decode('utf-8')
    return text


def get_reqs(fn):
    return [
        _.strip()
        for _ in open(os.path.join(CURRENT_DIR, fn)).readlines()
        if _.strip() and not _.strip().startswith('#')
    ]


setup(
    name="chimit",
    version=chimit.__version__,
    packages=['chimit'],
    entry_points=dict(console_scripts=['chimit=chimit.chimit:main', 'chimit-%s=chimit.chimit:main' % sys.version[:3]]),
    author="Chris Spencer",
    author_email="chrisspen@gmail.com",
    description="Fabric commands for simplifying server deployments",
    long_description=read_md('README.md'),
    long_description_content_type='text/markdown',
    license="MIT",
    url="https://github.com/chrisspen/chimit",
    #https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
    ],
    zip_safe=False,
    include_package_data=True,
    tests_require=get_reqs('requirements-test.txt'),
    test_suite='tests',
)

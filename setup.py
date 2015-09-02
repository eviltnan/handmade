#!/usr/bin/env python

# Support setuptools only, distutils has a divergent and more annoying API and
# few folks will lack setuptools.
from setuptools import setup, find_packages

# Version info -- read without importing
_locals = {}
with open('handmade/_version.py') as fp:
    exec (fp.read(), None, _locals)
version = _locals['__version__']

# Frankenstein long_description: version-specific changelog note + README
# todo: add readthedocs link
long_description = """
To find out what's new in this version of Handmade, please see `the changelog
<http://xxx/en/%s/xxx>`_.

%s
""" % (version, open('README.rst').read())

setup(
    name='handmade',
    version=version,
    description='Cross platform mobile and desktop application framework',
    license='MIT',

    long_description=long_description,
    author='Sergey Cheparev',
    author_email='sergey@cheparev.com',
    url='https://github.com/eviltnan/handmade',

    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'handmake = handmade.bin:handmake',
        ]
    },

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Android',
        'Operating System :: iOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
    ],
)

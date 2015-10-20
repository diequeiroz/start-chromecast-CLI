"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='startcast',
    
    version='0.1.0',

    description='Start chromecast apps from command line',
    long_description='Start chromecast apps from command line',
    
    url='https://github.com/diequeiroz/start-chromecast-CLI',

    author='Diego Queiroz',
    author_email='diego.queiroz@gmail.com',

    license='MIT',

    classifiers=[
    
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='chromecast application start cli',
    
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    
    install_requires=['pychromecast'],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'startcast=startcast:main',
        ],
    },
)
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='parsley',
    version='0.0.1',
    description='Library to transcode CAN messages and human-readable text',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/waterloo-rocketry/parsley',
    author='Waterloo Rocketry',
    author_email='contact@waterloorocketry.com',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',

        'License :: OSI Approved :: MIT License',

        'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows 10',

        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.10',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=find_packages(include=['parsley']),
    install_requires=requirements
)

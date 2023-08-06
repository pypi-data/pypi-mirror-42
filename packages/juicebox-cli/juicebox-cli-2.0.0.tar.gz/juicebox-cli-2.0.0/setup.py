from setuptools import setup, find_packages

from codecs import open
from os import path

from juicebox_cli import __version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

requirements = [
    'boto3==1.7.80',
    'certifi==2016.8.8',
    'click==7.0',
    'requests==2.11.0'
]

# Have setuptools generate the entry point
# wrapper scripts.
entry_points = {
    'console_scripts': [
        'juice=juicebox_cli.cli:cli',
    ],
}

setup(
    name='juicebox-cli',
    version=__version__,
    description='Juicebox CLI',
    long_description=long_description,
    author='Juice Analytics',
    author_email='tim.oguin@juiceanalytics.com',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=requirements,
    entry_points=entry_points,
    url='https://github.com/juiceinc/juicebox_cli',
    classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Office/Business',
          'Topic :: Internet',
          'Topic :: Communications :: File Sharing',
    ],
)

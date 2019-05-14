#!/usr/bin/python3
import setuptools

#To create the pypi distribution do..
#   python3 setup.py sdist bdist_wheel

# There are currently no dependencies so this is fine but note that if
# dependencies are added, this is a bad technique because setup will
# fail if those aren't installed first.
from lemminflect import __version__

with open('README.md', 'r') as fh:
    readme = fh.read()
    readme = readme.replace('![(icon)](docs/img/favicon.ico)', '')

setuptools.setup(
    name='lemminflect',
    version=__version__,
    author='Brad Jascob',
    author_email='bjascob@msn.com',
    description='A python module for English lemmatization and inflection.',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/bjascob/LemmInflect',
    # The following adds data files for the binary distribution only (not the source)
    # This impacts `setup bdist_wheel`.  Use the MANIFEST.in file to add data files to
    # the source package.  Also note that just using wildcards (ie.. *.csv) without the
    # path doesn't work unless there's an __init__.py in the directory because setup
    # doesn't look in there without it.
    include_package_data=True,
    package_data={'lemminflect':['resources/*']},
    packages=setuptools.find_packages(),
    install_requires=['numpy'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
    ],
)

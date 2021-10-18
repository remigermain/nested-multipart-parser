#!/usr/bin/env python3

import setuptools
import os
import sys
import subprocess


tags = subprocess.check_output("git tag -l | cat", shell=True).decode("utf-8")
version = list(filter(None, tags.split("\n")))[-1]

if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system('rm -rf dist nested_multipart_parser.egg-info')
    os.system("python setup.py sdist")
    if os.system("twine check dist/*"):
        print("twine check failed. Packages might be outdated.")
        print("Try using `pip install -U twine wheel`.\nExiting.")
        sys.exit()
    os.system("twine upload dist/*")
    sys.exit()


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nested-multipart-parser",
    version=version,
    author="rgermain",
    license='MIT',
    author_email='contact@germainremi.fr',
    description="A parser for nested data in multipart form",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/remigermain/nested-multipart-parser",
    project_urls={
        "Bug Tracker": "https://github.com/remigermain/nested-multipart-parser/issues",
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
    ],
    packages=["nested_multipart_parser"],
    python_requires=">=3.6",
)

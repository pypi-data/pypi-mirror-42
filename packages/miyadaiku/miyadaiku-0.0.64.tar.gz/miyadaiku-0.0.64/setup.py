import os
import sys
import re
import pathlib
from setuptools import setup, find_packages
from miyadaiku.common import setuputils

DIR = pathlib.Path(__file__).resolve().parent

requires = [
    "docutils", "pyyaml", "jinja2", "python-dateutil", "pygments",
    "pytz", "tzlocal", "happylogging>=0.0.5", "beautifulsoup4", "feedgenerator",
    "markdown>=3.0", "nbformat", "nbconvert", "watchdog",
]


entry_points = {
    'console_scripts': [
        'miyadaiku-start = miyadaiku.scripts.zichinsai:main',
        'miyadaiku-build = miyadaiku.scripts.muneage:main'
    ]
}

versionpy = DIR / 'miyadaiku/core/__version__.py'
version = re.search(r'"([\d.]+)"', versionpy.read_text())[1]

setup(
    name="miyadaiku",
    version=version,
    author="Atsuo Ishimoto",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    description='Miyadaiku - Flexible static site generator for Jinja2 artists',
    long_description=setuputils.read_file(DIR, 'README.rst'),
    url='https://github.com/miyadaiku/miyadaiku',
    project_urls={
        'Documentation': 'https://miyadaiku.github.io/',
        'Source': 'https://github.com/miyadaiku/miyadaiku',
    },
    python_requires='>=3.6',

    entry_points=entry_points,
    packages=list(setuputils.list_packages(DIR, 'miyadaiku')),
    package_data={
        '': setuputils.SETUP_FILE_EXTS,
    },
    install_requires=requires,
    include_package_data=True,
    zip_safe=False
)

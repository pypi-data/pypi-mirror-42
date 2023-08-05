import os

from setuptools import find_packages, setup

DESCRIPTION = (
    'Library to create spreadsheet files compatible with '
    'MS Excel 97/2000/XP/2003 XLS files, '
    'on any platform, with Python 2.7, 3.4+'
    )

CLASSIFIERS = [
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'License :: OSI Approved :: BSD License',
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Office/Business :: Financial :: Spreadsheet',
    'Topic :: Database',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    ]

KEYWORDS = (
    'xls excel spreadsheet workbook worksheet pyExcelerator'
    )

setup(
    name='xlwt_fix',
    version='1.3.1',
    maintainer='John Machin',
    maintainer_email='sjmachin@lexicon.net',
    url='http://www.python-excel.org/',
    download_url='https://pypi.org/project/xlwt/',
    description=DESCRIPTION,
    long_description=open(os.path.join(
        os.path.dirname(__file__), 'README.rst')
    ).read(),
    license='BSD',
    platforms='Platform Independent',
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=['six'],
)

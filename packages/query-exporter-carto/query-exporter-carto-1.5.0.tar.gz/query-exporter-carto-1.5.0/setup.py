from pathlib import Path

from setuptools import (
    find_packages,
    setup,
)

tests_require = ['pytest', 'pytest-asyncio', 'pytest-mock']

config = {
    'name': 'query-exporter-carto',
    'version': '1.5.0',
    'license': 'GPLv3+',
    'description': 'Publish Prometheus metrics generated from SQL queries (also for CARTO SQL API).',
    'long_description': Path('README.rst').read_text(),
    'author': 'Geographica.gs (fork from https://github.com/albertodonato/query-exporter)',
    'author_email': '',
    'maintainer': 'Daniel Ramirez',
    'maintainer_email': 'daniel.ramirez@geographica.com',
    'url': 'https://github.com/GeographicaGS/query-exporter',
    'packages': find_packages(include=['query_exporter', 'query_exporter.*']),
    'include_package_data': True,
    'entry_points': {
        'console_scripts': ['query-exporter = query_exporter.main:script']
    },
    'test_suite': 'query_exporter',
    'install_requires': [
        'aiohttp',
        'prometheus-client',
        'prometheus-aioexporter >= 1.5.1',
        'PyYaml',
        'SQLAlchemy == 1.3.0b2',
        'sqlalchemy_aio',
        'toolrack >= 2.1.0',
        'geographica-longitude == 1.0.0a1'
    ],
    'tests_require': tests_require,
    'extras_require': {
        'testing': tests_require
    },
    'keywords': 'sql metric prometheus exporter',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7', 'Topic :: Utilities'
    ]
}

setup(**config)

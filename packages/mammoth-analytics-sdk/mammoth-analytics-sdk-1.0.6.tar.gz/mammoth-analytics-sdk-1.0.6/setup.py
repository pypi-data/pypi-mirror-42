
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Mammoth Analytics sdk',
    'author': 'Mammoth developer',
    'author_email': 'developer@mammoth.io',
    'version': '1.0.6',
    'packages': ['MammothAnalytics'],
    'scripts': [],
    'name': 'mammoth-analytics-sdk',
    'install_requires': [
        'requests',
        'pytest',
        'names',
        'pydash'
    ]
}

setup(**config)

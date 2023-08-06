from setuptools import setup

setup(
    name='eppzy',
    description='EPP Client Library',
    keywords=['epp'],
    url='https://gitlab.com/aaisp/eppzy',
    author='David Honour',
    author_email='david@concertdaw.co.uk',
    version='0.0.0',
    license='LGPL3',
    packages=['eppzy'],
    install_requires=[
    ],
    extras_require={
        'test': ['pytest-flake8']
    },
    entry_points={}
)

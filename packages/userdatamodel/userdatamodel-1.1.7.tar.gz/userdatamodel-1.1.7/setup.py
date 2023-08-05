from setuptools import setup, find_packages

setup(
    name='userdatamodel',
    version='1.1.7',
    packages=find_packages(),
    install_requires=[
        'sqlalchemy>=0.9.9, <1.0.0',
        'cdislogging',
    ],
    scripts=[
        'bin/userdatamodel-init',
    ],
)

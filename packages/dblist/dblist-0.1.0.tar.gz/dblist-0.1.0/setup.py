"""Pip installation script."""

from setuptools import find_packages, setup

setup(
    name='dblist',
    description=('Storage of lists and Numpy arrays within relational '
                 'databases, using SQLAlchemy.'),
    version="0.1.0",
    author='Adam J. Plowman',
    packages=find_packages(),
    install_requires=[
        'sqlalchemy',
        'numpy',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha'
    ],
)

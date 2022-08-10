# https://flask.palletsprojects.com/en/2.1.x/tutorial/install/
# file for making project installable as python module

from setuptools import find_packages, setup

setup(
    name='money',
    version='1.0.0',
    packages=find_packages(),   # what packages to include
    include_package_data=True,  # also include static and templates folder
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
#-*- coding: utf-8 -*-

import os
try:
    from setuptools import setup, find_packages, Extension
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages, Extension

import os.path
src_folder= os.path.join(
    os.path.split(os.path.abspath(__file__))[0], 'src')
setup(
    name='neocortex-api-python',
    version="0.1",
    description='Meaningtool Neocortex API Python Client',
    author='Popego Team',
    author_email='contact@meaningtool.com',
    url='',
    install_requires=[ ],
    tests_require=[
            'nose'
            ],
    package_dir= {'' : 'src' },
    packages=find_packages(where=src_folder, exclude=['test', 'test.*']),
    include_package_data=True,
    test_suite='nose.collector',
    entry_points="""""",
    zip_safe=False
)



# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

with open('LICENSE') as f:
    license_txt = f.read()

setup(
    name='heiafr.isc.se.tpchecker',
    python_requires='>=3.6',
    description='Checker for Embedded System assignments',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Jacques Supcik',
    author_email='jacques.supcik@hefr.ch',
    url='https://gitlab.forge.hefr.ch/jacques.supcik/se12-checker',
    license=license_txt,
    py_modules=['check'],
    packages=['heiafr.isc.se.tpchecker'],
    include_package_data=True,
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    install_requires=[
        'Click',
        'jinja2',
        'weasyprint',
    ],
    entry_points='''
        [console_scripts]
        heiafr-check-se=check:main
    ''',

)

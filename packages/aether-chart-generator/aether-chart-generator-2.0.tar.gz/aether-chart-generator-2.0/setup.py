#!/usr/bin/env python3

from setuptools import setup


setup(
    name='aether-chart-generator',
    version='2.0',
    description='Generate helm chart for aether',
    url='http://github.com/ehealthafrica/ehealh-deployment',
    author='Oluwafemi Olofintuyi',
    author_email='devops@ehealthafrica.org',
    license='MIT',
    install_requires=['mako'],
    packages=['aether_chart_generator'],
    package_data={
        'aether_chart_generator': [
            'templates/*.tmpl.yaml',
            'templates/*.tmpl.txt',
            'templates/*.tmpl.tpl']},
    entry_points={
                'console_scripts': ['aether-chart-generator=aether_chart_generator.generator:main'],
                },
    zip_safe=False)

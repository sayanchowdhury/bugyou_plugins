# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requires = []

setup(
    name='bugyou_plugins',
    version='0.1.6',
    description='Plugins for bugyou, an automatic bug reporting tool',
    author='Sayan Chowdhury',
    author_email='sayanchowdhury@fedoraproject.org',
    url='https://github.com/sayanchowdhury/bugyou_plugins/',
    license='GPLv3',
    install_requires=requires,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
    entry_points={
        'console_scripts': [
            "bugyou-cntrl=bugyou_plugins.commands.cntrl:cntrl",
        ],
        'bugyou.plugins': [
            "autocloud = bugyou_plugins.plugins.autocloud.plugin:AutocloudPlugin",
        ],
        'bugyou.services': [
            "pagure = bugyou_plugins.services.pagure:PagureService",
        ]
    },
)

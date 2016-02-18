# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requires = []

setup(
    name='bugyou_plugins',
    version='0.1',
    description='Plugins for bugyou, an automatic bug reporting tool',
    author='Sayan Chowdhury',
    author_email='sayanchowdhury@fedoraproject.org',
    url='https://github.com/sayanchowdhury/bugyou_plugins/',
    license='GPLv3',
    install_requires=requires,
    packages=['bugyou_plugins'],
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

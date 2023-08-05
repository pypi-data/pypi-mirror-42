import os

from setuptools import setup, find_packages

setup(
    name='embarc_cli',
    version='1.0.2',
    description='This is a tool for Embedded Development with embARC',
    author='Jingru',
    author_email='1961295051@qq.com',
    keywords="embARC",
    url="",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            "embarc=embarc_tools.main:main",
        ]
    },
    python_requires='>=2.7.10,!=3.0.*,!=3.1.*,<4',
    classifiers=(
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'PyYAML',
        'colorama',
        'PrettyTable',
        'Jinja2',
        'beautifulsoup4'
    ],

    include_package_data = True,
)

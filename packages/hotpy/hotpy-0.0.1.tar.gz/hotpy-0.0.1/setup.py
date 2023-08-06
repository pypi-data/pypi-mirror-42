# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name="hotpy",
    version="0.0.1",
    description="hotpy",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Hotmart-Org/devops/hotpy",
    author="Jônatas Renan Camilo Alves",
    author_email="jonatas.alves@hotmart.com",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    keywords="hotpy scripts",
    packages=["hotpy"],
    install_requires=[],
    include_package_data=True,
    package_data={}
)

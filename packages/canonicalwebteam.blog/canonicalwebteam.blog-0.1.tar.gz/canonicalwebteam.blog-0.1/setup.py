#! /usr/bin/env python3

from setuptools import setup

setup(
    name="canonicalwebteam.blog",
    version="0.1",
    author="Canonical webteam",
    author_email="webteam@canonical.com",
    url="https://github.com/canonical-webteam/blog-flask-extension",
    description=(
        "Flask extension to add a nice blog to your website"
    ),
    long_description=open("README.md").read(),
    install_requires=[
        "canonicalwebteam.http==1.0.1",
        "Flask==1.0.2",
    ],
)

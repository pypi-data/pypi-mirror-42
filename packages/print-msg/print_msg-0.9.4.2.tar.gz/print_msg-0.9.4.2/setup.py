import setuptools
import os
import re
import shutil
from sys import argv

with open('README.md') as f:
    long_description = f.read()


def read(file: str) -> list:
    with open(file, encoding="utf-8") as r:
        return [i.strip() for i in r]


setuptools.setup(
    name="print_msg",
    version="0.9.4.2",
    author="Shvetsov Dmitry",
    author_email="shvetsovdmitry1996@gmail.com",
    description="Print colored status messages.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/shvetsovdmitry/print-msg",
    py_modules=['print_msg'],
    packages=setuptools.find_packages(),
    license="MIT",
    keywords="colored status messages module python",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    project_urls={
        "Tracker": "https://github.com/shvetsovdmitry/print-msg/issues",
        "Source": "https://github.com/shvetsovdmitry/print-msg",
    },
    python_requires="~=3.4",
    install_requires=read("requirements.txt"),
    extras_require={
        "termcolor": ["termcolor==1.1.0"],
    }
)

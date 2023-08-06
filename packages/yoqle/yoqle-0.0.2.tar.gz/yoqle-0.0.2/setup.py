import re
from setuptools import setup

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name = "yoqle",
    packages = ["yoqle"],
    entry_points = {
        "console_scripts": ['yoqle = yoqle.yoqle:main']
        },
    version = '0.0.2',
    description = "Command-line development streamlining tool.",
    long_description = long_descr,
    author = "Connor Curnin",
    author_email = "curnin@wisc.edu",
    url = "https://github.com/CTC97/yoqle",
    install_requires=[
        "termcolor",
        "pyfiglet>=0.7.5"
    ]
    )

import re
from setuptools import setup

setup(
    name = "yoqle",
    packages = ["yoqle"],
    entry_points = {
        "console_scripts": ['yoqle = yoqle.yoqle:main']
        },
    version = '0.0.7',
    description = "Command-line development streamlining tool.",
    author = "Connor Curnin",
    author_email = "curnin@wisc.edu",
    url = "https://github.com/CTC97/yoqle",
    install_requires=[
        "termcolor",
        "pyfiglet>=0.7.5"
    ]
    )

"""vater package installation setup."""
import os

from setuptools import find_packages, setup

DIR_PATH = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(DIR_PATH, "README.md"), encoding="utf-8") as file:
    long_description = file.read()

about = {}
with open(
    os.path.join(DIR_PATH, "vater", "__about__.py"), "r", encoding="utf-8"
) as file:
    exec(file.read(), about)


setup(
    name=about["__name__"],
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    license=about["__license__"],
    keywords=about["__keywords__"],
    download_url=about["__download_url__"],
    packages=find_packages("."),
    python_requires=">=3.11",
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.11",
    ],
)

"""vater package installation setup."""
import os

from pkg_resources import parse_requirements
from setuptools import find_packages, setup

DIR_PATH = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(DIR_PATH, "README.md"), encoding="utf-8") as file:
    long_description = file.read()

about = {}
with open(
    os.path.join(DIR_PATH, "src", "vater", "__about__.py"), "r", encoding="utf-8"
) as file:
    exec(file.read(), about)

with open(os.path.join(DIR_PATH, "requirements.txt"), encoding="utf-8") as file:
    requirements = [str(req) for req in parse_requirements(file.read())]

with open(os.path.join(DIR_PATH, "requirements-dev.txt"), encoding="utf-8") as file:
    requirements_dev = [str(req) for req in parse_requirements(file.read())]

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
    package_dir={"": "src"},
    packages=find_packages("src"),
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={"dev": requirements_dev},
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={"console_scripts": "vater=vater.cli:cli"},
)

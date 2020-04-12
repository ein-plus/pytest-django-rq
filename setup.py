import os
from pathlib import Path

from setuptools import setup, find_packages

PACKAGE_NAME = "pytest-django-rq"

here = Path(__file__).parent

long_description = (here / "README.md").read_text(encoding="utf-8")

about = {}
path = here / PACKAGE_NAME.replace('-', '_').replace('.', os.path.sep) / "version.py"
exec(path.read_text(encoding="utf-8"), about)

required = ['pytest-mock', 'fakeredis']

entry_points = """
[pytest11]
pytest_django_rq = pytest_django_rq
"""

setup(
    name=PACKAGE_NAME,
    version=about['__version__'],
    description="A pytest plugin to help writing unit test for django-rq",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Qiangning Hong",
    author_email="hongqn@ein.plus",
    url="https://github.com/ein-plus/pytest-django-rq",
    setup_requires=['setuptools>=38.6.0'],  # long_description_content_type support
    python_requires=">=3.6",  # f-string support
    packages=find_packages(exclude=['tests']),
    entry_points=entry_points,
    install_requires=required,
    license='MIT',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)

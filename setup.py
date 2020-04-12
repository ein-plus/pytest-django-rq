import os
from pathlib import Path

from setuptools import setup, find_packages

PACKAGE_NAME = "pytest-django-rq"

here = Path(__file__).parent

long_description = (here / "README.md").read_text(encoding="utf-8")

about = {}
exec(
    (
        here / PACKAGE_NAME.replace('-', '_').replace('.', os.path.sep) / "version.py"
    ).read_text(encoding="utf-8"),
    about,
)

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
    author_email="hongqn@gmail.com",
    url="https://github.com/hongqn/pytest-django-rq",
    setup_requires=['setuptools>=38.6.0'],  # long_description_content_type support
    python_requires=">=3.6",  # f-string support
    packages=find_packages(exclude=['tests']),
    entry_points=entry_points,
    install_requires=required,
    license='MIT',
)

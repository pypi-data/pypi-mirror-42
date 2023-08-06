# pylint: disable=attribute-defined-outside-init
import sys
import os
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import netcli as package


def parse_requirements(requirements_file):
    with open(requirements_file) as f:
        return f.read().strip().split('\n')


class PyTest(TestCommand):

    def initialize_options(self):
        TestCommand.initialize_options(self)

        self.pytest_args = [
        ]

        self.lint_args = [
            '--flake8',
            '--pylint'
        ]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.pytest_args.extend(self.lint_args)

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name=package.__name__,
    version=package.__version__,
    python_requires='>=3.5',
    author=package.__author__,
    author_email=package.__author_email__,
    description=package.__description__,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'netcli = netcli.cli:cli'
        ]
    },
    install_requires=parse_requirements(os.path.join('requirements', 'requirements.txt')),
    tests_require=parse_requirements(os.path.join('requirements', 'test_requirements.txt')),
    cmdclass={'test': PyTest},
    test_suite='tests',
    license='MIT',
    keywords=['Git', 'GitHub', 'automation', 'networking', 'netmiko'],
    classifiers=[
        "Development Status :: 4 - Beta",

        "Environment :: Console",

        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",

        "Topic :: Internet :: WWW/HTTP",
    ],
)

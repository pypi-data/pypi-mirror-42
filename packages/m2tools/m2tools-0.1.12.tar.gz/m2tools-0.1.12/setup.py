import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

install_requires = ['click']

if sys.version_info < (3, 0, 0):
    raise RuntimeError("m2tools requires Python 3.0.0+")


def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def run_tests(self):
        import shlex

        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


tests_require = install_requires + ['pytest', 'pytest-timeout']

args = dict(
    name='m2tools',
    version='0.1.12',
    description='Magento 2 python toolkit',
    classifiers=['Topic :: Internet :: WWW/HTTP', 'Topic :: Software Development :: Libraries :: Python Modules', 'Intended Audience :: Developers'],
    author='Peter Samoilov',
    author_email='xserv@gmail.com',
    maintainer='Peter Samoilov',
    maintainer_email='xserv@gmail.com',
    license='MIT',
    packages=['m2tools'],
    install_requires=install_requires,
    tests_require=tests_require,
    include_package_data=True,
    cmdclass=dict(test=PyTest)
)
setup(**args)
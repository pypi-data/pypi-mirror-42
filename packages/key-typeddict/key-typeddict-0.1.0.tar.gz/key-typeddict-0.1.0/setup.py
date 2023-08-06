import sys
from distutils.core import setup

from setuptools import find_packages


dependencies = [
    'mypy>=0.670'
]
if sys.version_info[:2] < (3, 7):
    # dataclasses port for 3.6
    dependencies += ['dataclasses']

setup(
    name="key-typeddict",
    version="0.1.0",
    description='mypy_extensions.TypedDict with some additional features',
    url="https://github.com/mkurnikov/key-typeddict",
    author="Maksim Kurnikov",
    author_email="maxim.kurnikov@gmail.com",
    license='MIT',
    install_requires=dependencies,
    packages=['key_typeddict'],
    package_data={'key_typeddict': ['py.typed', 'core.pyi']},
    zip_safe=False
)

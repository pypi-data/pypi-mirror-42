"""Config file."""
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='python3_authjwt',
    version='0.0.1',
    description='Flask JWT auth security for Appengine',
    url='https://github.com/claudiokc/python3-authjwt',
    author='Claudio J. Cáceres',
    author_email='catocaceres@hotmail.com',
    license='MIT',
    packages=['python3_authjwt'],
    install_requires=['pyjwt', 'Flask'],
    zip_safe=False
)

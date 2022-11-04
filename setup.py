from setuptools import setup
from setuptools import find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    use_scm_version=True,
    packages=find_packages(),
    long_description=readme,
    long_description_content_type='text/markdown',
)

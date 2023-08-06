from setuptools import setup, find_packages
import re, os



requirements = []
with open('../code/requirements.txt') as f:
  requirements = f.read().splitlines()



version = ''
with open('../code/pyfw/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

readme = ''
with open('README.md') as f:
    readme = f.read()



setup(
        name = "pyfw",
        version = version,
        keywords = ("pip", "cmcc","python", "pyfw", "framework"),
        description = "python framework",
        long_description = readme,
        license = "MIT Licence",

        url = "https://github.com/wenanguo/pyfw",
        author = "Andrew Wen",
        author_email = "79912844@qq.com",

        packages = find_packages(),
        include_package_data = True,
        platforms = "any",
        install_requires = requirements


)

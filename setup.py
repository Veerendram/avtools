from os import path
from setuptools import setup, find_packages

with open(path.join(path.dirname(__file__),
                    'README.md')) as f:
    long_description = f.read()

setup(
    name="avtools",
    version="1.0.0",
    author="Veerendra",
    author_email="",
    description="MediaQuality for Automation",
    packages=find_packages(),
    install_requires=['psutil', 'pillow', 'watchdog',
                      'pyyaml', 'pyqrcode', 'python-resize-image',
                      'six', 'bs4', 'numpy'],
    long_description=long_description,
    zip_safe=False
)

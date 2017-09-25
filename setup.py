from install_packages import install_scikit_image
from os import path
from setuptools import setup, find_packages
from setuptools.command.install import install

with open(path.join(path.dirname(__file__),
                    'README.md')) as f:
    long_description = f.read()


class Installer(install):
    """
    Custom installer to install dependencies
    """
    def run(self):
        install.run(self)
        self.execute(install_scikit_image, [],
                     msg="Installing Scikit-image library")

setup(
    name="avtools",
    version="1.0.0",
    author="Veerendra",
    author_email="",
    description="MediaQuality for Automation",
    packages=find_packages(),
    install_requires=['psutil', 'pillow', 'watchdog',
                      'pyyaml', 'pyqrcode', 'python-resize-image',
                      'six', 'bs4', 'numpy', 'pytest'],
    long_description=long_description,
    zip_safe=False,
    cmdclass={"install": Installer}
)

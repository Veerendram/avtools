# -*- coding: utf-8 -*-
from os import path, mkdir, getcwd
import pip
import requests


def install_scikit_image():
    """
    As we have unofficial wheel support for Scikit
    image library for windows.
    It's installed from github location
    :return:
    """
    package = r"scikit_image-0.13.0-cp27-cp27m-win_amd64.whl"

    si_url = str("https://github.com/Veerendram/"
                 "thirdpary_packages_internal/raw/master/{}").format(package)

    print "Downloading scikit image: {}".format(si_url)
    print "getcwd: {}".format(getcwd())
    download_location = "{}\downloads".format(getcwd())
    save_file_as = "{}\{}".format(download_location, package)

    if not path.isfile(path.join(download_location, package)):
        if not path.isdir(download_location):
            mkdir(download_location)

        # urlretrieve(url=si_url, filename=save_file_as)
        print "downloading with requests"
        r = requests.get(si_url)
        with open(save_file_as, "wb") as dwnld:
            dwnld.write(r.content)
    print "Installing {}".format(save_file_as)
    cmd = save_file_as
    pip.main(['install', cmd, '--upgrade', '--force-reinstall',
              '--no-cache-dir', '--no-deps'])

if __name__ == '__main__':
    install_scikit_image()

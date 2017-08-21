import platform
import subprocess
from os import path, listdir, environ
import os

ZBAR_IMG = path.join("bin", "zbarimg")


def get_windows_zbar_path():
    """
    Returns the path for the zbar executable on windows.
    Looks in both program files directories to make sure it can be located.
    The only MSI installer for silent installation that could be found
    installs a version to python, so this will allow for whatever version
    is installed to be used.
    :return:
    """
    if path.exists(path.normpath(r"C:\Python27\zbarimg.exe")):
        zbar_path = path.normpath(r"C:\Python27\zbarimg.exe")
        print "ZBAR PATH: {}".format(zbar_path)
        return zbar_path

    elif path.exists(path.join(environ["PROGRAMFILES(X86)"], "ZBar")):
        zbar_dir = path.join(environ["PROGRAMFILES(X86)"], "ZBar")

    elif path.exists(path.join(environ["PROGRAMFILES"], "ZBar")):
        zbar_dir = path.join(environ["PROGRAMFILES"], "ZBar")

    else:
        raise IOError(
            "Could not locate zbar installation. Please use the installer "
            "script to download and install the correct version."
        )
    zbar_path = path.join(zbar_dir, ZBAR_IMG)
    print "ZBAR PATH: {}".format(zbar_path)
    return zbar_path


class QrCode(object):

    def decode_qr_code(self, qr_path):
        """
        Decodes a QR code passed by the file_path attribute, and returns it's
        text value.
        :param qr_path:
        :return:
        """
        if not path.exists(qr_path):
            raise IOError(
                "Could not locate the file '{}'. Please ensure the QR code you"
                " are trying to decode exists.".format(qr_path)
            )
        os_name = platform.system()

        if os_name == "Windows":
            zbar_exe = get_windows_zbar_path()
        else:
            raise OSError("Unrecognised operating system '{}'.".format(os_name))

        response = subprocess.check_output([zbar_exe, '-q', qr_path])

        # The response is returned in the format "QR-Code:<Value>".
        # We don't need the 'QR-Code:' part, just the actual value, so trim off
        # the start.
        response = response[8:]
        print "QR CODE VALUE: {}".format(response)
        return response




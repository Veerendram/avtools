import platform
import subprocess
from os import path, environ

ZBAR_IMG = path.join("bin", "zbarimg")


def get_windows_zbar_path():
    """
    Returns the path for the zbar executable on windows.
    Looks in both program files directories to make sure it can be located.
    However, zbar works with 32bit windows
    :return:
    """
    if path.exists(path.normpath(r"C:\Python27\zbarimg.exe")):
        zbar_path = path.normpath(r"C:\Python27\zbarimg.exe")
        print "ZBAR PATH: {}".format(zbar_path)
        return zbar_path

    elif path.exists(path.join(environ["PROGRAMFILES(X86)"], "ZBar")):
        zbar_install_dir = path.join(environ["PROGRAMFILES(X86)"], "ZBar")

    elif path.exists(path.join(environ["PROGRAMFILES"], "ZBar")):
        zbar_install_dir = path.join(environ["PROGRAMFILES"], "ZBar")

    else:
        raise IOError(
            "Could not locate zbar installation."
        )
    zbar_path = path.join(zbar_install_dir, ZBAR_IMG)
    print "ZBAR PATH: {}".format(zbar_path)
    return zbar_path


class QrCode(object):

    def decode_qr_code(self, qr_file_path):
        """
        Decodes a QR code passed by the file_path attribute, and returns it's
        text value.
        :param qr_file_path:
        :return:
        """
        if not path.exists(qr_file_path):
            raise IOError(
                "Could not locate the file '{}'. Please ensure the QR code you"
                " are trying to decode exists.".format(qr_file_path))
        os_name = platform.system()

        if os_name == "Windows":
            zbar_exe = get_windows_zbar_path()
        else:
            raise OSError("Unrecognised operating system '{}'.".format(os_name))

        response = subprocess.check_output([zbar_exe, '-q', qr_file_path])
        decoded_qrcode_value = response[8:]
        print "QR CODE VALUE: {}".format(decoded_qrcode_value)
        return decoded_qrcode_value

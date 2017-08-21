import hashlib


class fileLib(object):
    """Library containing miscellaneous tools to handle a
    nd check files, on-top of the existing OperatingSystem built-in library.
       As of version 0.1, this library contains keywords for:
       - Getting files checksum (sha256).
    """

    def __init__(self):
        return

    def get_file_checksum(self, path):
        """Return sha256 hash of a given full file path."""
        hasher = hashlib.sha256()
        print "Calculating hash of: {}".format(str(path))
        with open(path, 'rb') as afile:
            buf = afile.read()
            hasher.update(buf)
        hash = hasher.hexdigest()
        print "Hash of: {} is {}".format(str(path), str(hash))
        return hash

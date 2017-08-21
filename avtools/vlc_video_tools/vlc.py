import os
import tempfile
import platform
import psutil


class VLC(object):
    """
    Super class for handling VLC
    """
    def __init__(self):

        self.tmpFolder = tempfile.mkdtemp()
        self.os_name = platform.system()

        if self.os_name == 'Darwin':
            self.vpath = '/Applications/VLC.app/Contents/MacOS/VLC'
            self.vlc_process_name = 'VLC'

        elif self.os_name == 'Windows' and os.path.exists('C:\\PROGRA~1\\VideoLAN\\VLC\\vlc.exe'):
            self.vpath = r'C:\\PROGRA~1\\VideoLAN\\VLC\\vlc.exe'
            self.vlc_process_name = 'vlc.exe'

        elif self.os_name == 'Windows' and os.path.exists('C:\\PROGRA~2\\VideoLAN\\VLC\\vlc.exe'):
            self.vpath = r'C:\\PROGRA~2\\VideoLAN\\VLC\\vlc.exe'
            self.vlc_process_name = 'vlc.exe'

        elif self.os_name == 'Linux':
            self.vpath = '/usr/bin/vlc'
            self.vlc_process_name = 'VLC'

        else:
            self.vpath = 'vlc'

        if not os.path.isfile(self.vpath):
            print "Could not find VLC executable location"
            raise ValueError("Could not find VLC executable location")
        print "Found VLC executable : "+repr(self.vpath)
        return

    def vlc_process_status(self):
        """
        Get VLC Process Status .
        Returns True if exists, else False
        """
        for p in psutil.process_iter():
            if self.vlc_process_name in p.name():
                print "vlc.py: VLC Process exists, it has process id {}".format(p.pid)
                return True
        print "vlc.py: VLC didn't start, Please check command"
        return False

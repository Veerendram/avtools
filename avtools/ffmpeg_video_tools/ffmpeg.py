from os import path
import tempfile
import platform


class FFMPEG(object):
    """
    Class for handling ffmpeg, ffprobe binaries and subclass can use
    this for encoders, decorders, transcoding, extracting video and audio
    information.
    """

    def __init__(self):

        self.temp_folder = tempfile.mkdtemp()
        self.os_name = platform.system()

        if self.os_name == 'Windows' and path.exists(
                "C:\\ffmpeg\\bin"):
            self.ffmpeg_path = r"C:\\ffmpeg\\bin\\ffmpeg.exe"
            self.ffprobe_path = r"C:\\ffmpeg\\bin\\ffprobe.exe"

        elif self.os_name == 'Darwin':
            raise NotImplementedError("TODO: Need MAC implementation of  "
                                      "FFMPEG")

        elif self.os_name == 'Linux':
            raise NotImplementedError("TODO: Need Linux implementation of  "
                                      "FFMPEG")
        else:
            raise OSError("Check your Operatng system")

        if not path.isfile(self.ffmpeg_path):
            err = "Could not find ffmpeg executable file, please check " \
                  "ffmpeg installation"
            print "err"
            raise Exception(err)
        print "FFMPEG binary used : {}".format(self.ffmpeg_path)
        return



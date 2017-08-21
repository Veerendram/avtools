from os import path, makedirs
import shlex
import multiprocessing
import psutil
import platform
import subprocess

from avtools.ffmpeg_video_tools.ffmpeg import FFMPEG


class ScreenRecorder(FFMPEG):
    """
    Class used to start and stop screen capture using ffmpeg.
    """

    def __init__(self, video_file_name, video_format,
                 video_folder=None):
        super(ScreenRecorder, self).__init__()

        self.video_file_name = video_file_name

        self.video_format = video_format.lower()
        if video_folder is None:
            self.video_folder = self.temp_folder
        else:
            self.video_folder = video_folder
            if not path.exists(self.video_folder):
                makedirs(self.video_folder)
        self.video_folder = video_folder

        if self.video_format == 'ts':
            self.video_file_name += '.ts'

        elif self.video_format == 'mp4':
            self.video_file_name += '.mp4'
        else:
            raise NotImplementedError(
                "Screen Capture supports ts and mp4 format")

        self.video_file_path = path.join(self.video_folder,
                                         self.video_file_name)
        # TODO: Need Refactoring of the command to avoid a/v sync issues while capturing in mp4 format

        mp4_cmd_template = """{} -y -rtbufsize 5000M -r 24 -async 1 -f dshow
                -i video="screen-capture-recorder":audio="virtual-audio
                -capturer" -acodec aac -strict experimental -ar 44100 -ac 2
                -b:a 128k -vcodec libx264 -qscale:v 0 -b:v 800k {} """

        ts_cmd_template = """{} -y -rtbufsize 2000M -r 24 -async 1 -f dshow
                -i video="screen-capture-recorder":audio="virtual-audio-capturer"
                -acodec aac -strict experimental -ar 44100 -ac 2 -b:a 128k
                -vcodec mpeg2video  -qscale:v 0 -b:v 800k {} """

        if self.video_format == 'ts':
            capture_command = ts_cmd_template.format(self.ffmpeg_path,
                                                     self.video_file_path)
            self.screen_capture_command = shlex.split(capture_command)
            print "ffmpeg command line for screen capture/recording: {}\n". \
                format(self.screen_capture_command)

        elif self.video_format == 'mp4':
            # TODO: once command is calibrated, remove this error.
            raise NotImplementedError(
                "Screen capture/recorder with H264 video Codec "
                "and AAC Audio Codec needs refactoring")

    def __start(self):
        """
        Starts screen capture process
        :return :
        """
        process_number = subprocess.Popen(self.screen_capture_command)
        return process_number

    def start_ffmpeg_screen_capture(self):
        """
        Starts Screen Capture using FFMPEG and direct show software's.
        We are using python multiprocessing module to start/open the screen
        capture "start" method,
        :return multiprocess_id:
        """
        # TODO: Need better way to handle process, rather than doing with multiprocess or threading.

        multiprocess_id = multiprocessing.Process(
            name="FFMPEG ScreenRecorderFfmpeg",
            target=self.__start)
        multiprocess_id.daemon = True
        multiprocess_id.start()

        print "Started screen capture with alias"
        print "Multiprocessing process is alive: {}".format(
            multiprocess_id.is_alive())
        return multiprocess_id
        # return  [screen_capture_file, pid]

    def stop_ffmpeg_screen_capture(self, multiproc):
        """
        Terminates the multiprocess.
        To terminate Mp4 streams/capture, if psutil terminate is used ,
        file gets corrupted. So, sending signal CRTL_BREAK_EVENT doesn't
        corrupt the file.
        To terminate ts streams/capture, psutil terminate works.
        :param multiproc:
        :return:
        """
        multiproc.terminate()
        multiproc.join()
        if platform.system() == "Windows":
            ffmpeg_service = "ffmpeg.exe"
        else:
            # TODO:Need to handle for MAC and Linux Environments
            ffmpeg_service = "ffmpeg"
        for proc in psutil.process_iter():
            if proc.name() == ffmpeg_service:
                if self.video_format == 'mp4':
                    proc.send_signal(psutil.signal.CTRL_BREAK_EVENT)
                elif self.video_format == 'ts':
                    proc.terminate()

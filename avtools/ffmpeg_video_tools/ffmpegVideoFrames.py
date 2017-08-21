import shlex
import subprocess
import multiprocessing
from os import path, makedirs, listdir

from avtools.ffmpeg_video_tools.ffmpeg import FFMPEG
from avtools.utils.processInfo import ProcessInfo

PROCESS_QUERY_INFROMATION = 0x1000


class ExtractVideoFrames(FFMPEG):
    """
    Used
    and starting the frame extraction process.
    """

    def __init__(self, video_file, rate,
                 start_time=None, stop_time=None, frames_path=None):

        super(ExtractVideoFrames, self).__init__()
        self.video_file = video_file

        # TODO : 1. Folder Creation is a common functionality across all
        # libraries, better to handle in a main __init__.py  of tools or
        # add a utility

        if frames_path is None:
            self.frames_folder = self.temp_folder
        else:
            self.frames_folder = frames_path
            if not path.exists(self.frames_folder):
                makedirs(self.frames_folder)

        self.ratio = rate
        self.start_time = start_time
        self.stop_time = stop_time
        self.formatted_frames_path = r"{}".format(
            path.normpath(self.frames_folder))

        if start_time is None and stop_time is None:
            start_stop_command = ""

        elif start_time is None:
            start_stop_command = "-to {}".format(stop_time)

        elif stop_time is None:
            start_stop_command = "-ss {}".format(start_time)

        else:
            start_stop_command = "-ss {} -to {}".format(
                start_time, stop_time)

        cmd_string = """{ffmpeg_exe} -accurate_seek -i '{file}'
                        -r {ratio} {start_stop} -threads 0 -s hd720
                        '{output}\\img-%05d.png' """

        frames_cmd = cmd_string.format(
            ffmpeg_exe=self.ffmpeg_path, file=self.video_file,
            ratio=self.ratio, start_stop=start_stop_command,
            output=self.formatted_frames_path
        )

        print "ffmpeg command line: {}\n".format(frames_cmd)
        self.start_frames = shlex.split(frames_cmd)
        print "Final extract command: {}\n".format(self.start_frames)

    def __start(self):
        """
        Starts the frame extraction subprocess
        :return:
        """
        process_number = subprocess.Popen(self.start_frames)
        return process_number

    def start_video_frames_extraction(self):
        """
        Starts video frames extraction process.
        User should provide scene_ratio (frame rate) value, so that frames are
        extracted based on this value.

        :return frames_folder: returns path where frames are stored ( same
        as user provided), if user doesn't provide frames_folder ,
        temp_folder created by the ffmpeg.py is returned.
        :return frames_count: Number of Frames extracted
        """
        multiprocess_id = multiprocessing.Process(name="FFMPEG VideoFrames",
                                                  target=self.__start)
        # multiprocess_id.daemon = True
        multiprocess_id.start()
        multiprocess_id.join()
        print "Started frames extraction"
        # Check for the ffmpeg process to stop and return with extracted
        # frames folder and frames count
        process_info = ProcessInfo()
        while process_info.get_process_status("ffmpeg"):
            continue
        frames_count = self.get_extracted_frames(self.frames_folder)
        return [self.frames_folder, frames_count[1]]

    @staticmethod
    def get_extracted_frames(frames_folder):
        """
        Checks for the folder where frames are created and returns created
        frames(images) count.
        NOTE: Testers should make sure they use this method based on the
        video length and frame extraction time.
        :param frames_folder:
        :return: return the status and number of frames available (as list)
        """
        """
        TODO: May have to implement a timer functionality to wait until
        frames extraction is complete. --TBD--
        """
        status = False
        num_files = 0
        if path.isdir(frames_folder):
            num_files = len([f for f in listdir(frames_folder)
                             if
                             path.isfile(path.join(frames_folder, f))])
            if num_files != 0:
                status = True
            return [status, num_files]

        return [status, num_files]

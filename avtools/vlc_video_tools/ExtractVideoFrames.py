import shlex
from os import path, listdir, makedirs
import subprocess
from avtools.vlc_video_tools.vlc import VLC


class _ExtractFrames(VLC):
    """
    Used by VideoFrames class for variables initialization
    and starting the frame extraction process.
    """

    def __init__(self, video_file, scene_ratio,
                 start_time=None, stop_time=None, frames_path=None):

        super(_ExtractFrames, self).__init__()
        self.video_file = video_file
        """
        TODO :
        1. Folder Creation is a common functionality across all
        libraries, better to handle in a main __init__.py  of tools or
        add a utility
        2. VLC Logging should be enabled using "File logging" command line
        options.
        """
        if frames_path is None:
            frames_folder = self.tmpFolder
        else:
            frames_folder = frames_path
            if not path.exists(frames_folder):
                makedirs(frames_folder)

        self.ratio = scene_ratio
        self.start_time = start_time
        self.stop_time = stop_time
        self.formatted_frames_path = r"{}".format(path.normpath(frames_folder))

        if self.os_name == "Windows":
            quiet_command = "--dummy-quiet"
        else:
            quiet_command = "--quiet"

        if start_time is None and stop_time is None:
            start_stop_command = ""

        elif start_time is None:
            start_stop_command = "--stop-time={}".format(stop_time)

        elif stop_time is None:
            start_stop_command = "--start-time={}".format(start_time)

        else:
            start_stop_command = "--start-time={} --stop-time={}".format(
                start_time, stop_time)

        cmd_string = """{exe} '{file}' -I dummy {quiet} --video-filter=scene
            --scene-format=png --scene-ratio={ratio} {start_stop}
            --scene-prefix=auto-img- --vout=dummy --aout=dummy
            --scene-path='{output}' vlc://quit"""

        frames_cmd = cmd_string.format(
            exe=self.vpath, file=self.video_file, quiet=quiet_command,
            ratio=self.ratio, start_stop=start_stop_command,
            output=self.formatted_frames_path
        )

        print "VLC command line: {}\n".format(frames_cmd)
        self.start_frames = shlex.split(frames_cmd)
        print "Final extract command: {}\n".format(self.start_frames)

    def start(self):
        """
        Starts the frame extraction process using robot framework process
        library
        :return:
        """
        if hasattr(self, 'process'):
            err = "video '{}' Frames Extraction has already " \
                  "started.".format(self.video_file)
            print err
            raise Exception(err)

        process_number = subprocess.Popen(self.start_frames)
        return process_number


class VideoFrames(object):
    """
    VideoFrames is a video library to extract video frames (as Images) from
    a given video file. Uses VLC to extract frames.
    Tested and Works well with VLC 2.2.4 and 3.0.0(GIT Version)
    """

    def __init__(self):
        pass

    def __setup_video_frames_extraction(self, video_file, scene_ratio,
                                        start_duration=None, stop_duration=None,
                                        frames_folder=None):
        """
        Setup video frame extraction from the given video file.
        """
        frames = _ExtractFrames(video_file, scene_ratio, start_time=start_duration,
                                stop_time=stop_duration, frames_path=frames_folder)

        print "Initialize video frames extraction"
        return frames

    def start_video_frames_extraction(self, video_file, scene_ratio,
                                      start_duration=None, stop_duration=None,
                                      frames_folder=None):
        """
        Starts video frames extraction process.
        User should provide scene_ratio value, so that frames are extracted
        based on this value.
        Reference: https://wiki.videolan.org/VLC_command-line_help/
            --scene-ratio=<integer [1 .. 2147483647]> Recording ratio
            Ratio of images to record. 3 means that one image out of three is
            recorded.
        :param video_file:
        :param scene_ratio:
        :param start_duration
        :param stop_duration
        :param frames_folder:
        :return frames_folder: returns path where frames are stored ( same
        as user provided), if user doesn't provide frames_folder ,
        temp_folder created by the VLC.py is returned.
        :return pid: Process ID
        """

        frames = self.__setup_video_frames_extraction(video_file, scene_ratio, start_duration,
                                                      stop_duration, frames_folder)

        pid = frames.start()
        print "Started frames extraction"
        return [frames_folder, pid]

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

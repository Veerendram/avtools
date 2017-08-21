import shlex
from os import path, makedirs, stat
from platform import system
import subprocess

from avtools.vlc_video_tools.vlc import VLC


class _ExtractAudioFrames(VLC):
    """
    Used by AudioExtraction class for variables initialization
    and starting the audio Transcoding/conversion process.
    """

    def __init__(self, video_file, acodec,
                 audio_file, audio_file_path=None):

        super(_ExtractAudioFrames, self).__init__()
        self.video_file = video_file
        self.audio_file = audio_file
        self.audio_codec = acodec.lower()
        """
        TODO :
        1. Folder Creation is a common functionality across all
        libraries, better to handle in a main __init__.py  of tools or
        add a utility
        2. VLC Logging should be enabled using "File logging" command line
        options.
        """

        if audio_file_path is None:
            self.audio_folder = self.tmpFolder
        else:
            self.audio_folder = audio_file_path
            if not path.exists(self.audio_folder):
                makedirs(self.audio_folder)

        if system() == "Windows":
            quiet_command = "--dummy-quiet"
        else:
            quiet_command = "--quiet"

        if self.audio_codec == 'mp3':
            self.audio_file += '.mp3'
            self.full_audio_file_path = path.join(self.audio_folder,
                                                  self.audio_file)
            acodec = "acodec={}".format(self.audio_codec)
            mux = "mux=raw"
            destination_file = "dst='{}'".format(self.full_audio_file_path)

        elif self.audio_codec == 'wav':
            wav_codec = 's16l'
            self.audio_file += '.wav'
            self.full_audio_file_path = path.join(self.audio_folder,
                                                  self.audio_file)
            acodec = "acodec={}".format(wav_codec)
            mux = "mux=wav"
            destination_file = "dst='{}'".format(self.full_audio_file_path)

        else:
            raise ValueError("Please provide valid audio_codec values. "
                             "Value should be either mp3 or wav")

        cmd_template = """{} -I dummy {quiet} --no-sout-video
            --sout-audio --sout-keep --sout "#transcode{{{acodec},\
            vcodec=dummy}} :std{{access=file,{mux},{destination_file}}}"
            file:///{source_file} vlc://quit"""

        audio_cmd = cmd_template.format(self.vpath, quiet=quiet_command,
                                        acodec=acodec, mux=mux,
                                        destination_file=destination_file,
                                        source_file=self.video_file)

        print "VLC command line: {}\n".format(audio_cmd)
        self.audio_extraction_cmd = shlex.split(audio_cmd)
        print "Final extract command: {}\n".format(
            self.audio_extraction_cmd)

    def start(self):
        """
        Starts the audio extraction/conversion process using robot framework
        process library
        :return:
        """

        if hasattr(self, 'process'):
            err = "Audio extraction has already been started."
            print err
            raise Exception(err)

        proc = subprocess.Popen(self.audio_extraction_cmd)
        proc.wait()


class AudioExtraction(object):
    """
    AudioExtraction is a a/v library required for converting an video file
    in to audio file. Currently this module supports mp3 and wav audio
    codec format.
    Tested with VLC Ver2.2.4, 2.2.5 and 3.0.0(Nightly GIT Version)
    Suggested audio codec is wav format as it is lossless and tanscoding
    time is less compared to mp3

    Transcodes video and extracs only audio frames,
    As this class Transcodes, this module should support all audio codec
    (with in video) as input.
    """

    def __init__(self):
        pass

    def __setup_audio_extraction(self, video_file, audio_codec,
                                 audio_frames_file, audio_frames_folder=None):
        """
        Initializes video to audio conversion from the given video file.
        alias is custom name given to process to identify active process.
        :param video_file:
        :param audio_codec:
        :param audio_frames_file:
        :param audio_frames_folder:
        :return audio_frames_folder: Path where extracted audio are stored
        """

        audio_frames = _ExtractAudioFrames(video_file, audio_codec,
                                           audio_frames_file,
                                           audio_frames_folder)
        print "Initialize video frames extraction"
        return audio_frames

    def start_audio_extraction(self, video_file, audio_codec,
                               audio_frames_file, audio_frames_folder):
        """
        Starts audio conversion process
        :param video_file:
        :param audio_codec:
        :param audio_frames_file:
        :param audio_frames_folder:
        :return pid: Process ID:
        :return
        """

        audio_file = self.__setup_audio_extraction(video_file,
                                                   audio_codec,
                                                   audio_frames_file,
                                                   audio_frames_folder)
        pid = audio_file.start()
        print "Started audio extraction with alias"
        return [audio_file, pid]

    @staticmethod
    def get_audio_file_size(audio_file_folder, audio_file):
        """
        Checks for the file in the given folder where transcoded/converted
        audio file is created and returns created file size in MB.
        If file size is 0 and if file doesn't exist, error is thrown.
        NOTE: Testers should make sure they use this method based on the
        video length and audio extraction time.
        :param audio_file_folder:
        :param audio_file:
        :return audio_file_size:
        """

        file_absolute_path = path.join(audio_file_folder, audio_file)
        if path.isfile(file_absolute_path):
            print "Audio file {} exist ".format(file_absolute_path)
            audio_file_size = round((stat(file_absolute_path).st_size) / (1024 * 1024.0), 2)
            print "File Size of {} is {}".format(audio_file,
                                                 audio_file_size)
            if audio_file_size > 0:
                return audio_file_size
            elif audio_file_size == 0:
                raise ValueError("Audio file exist {} but file size is zero."
                                 "Please check VLC audio transcoding/extraction"
                                 " command ".format(file_absolute_path))
        else:
            raise ValueError("Unable to find file {}. Please check "
                             "VLC audio transcoding/extraction command".format(
                            file_absolute_path))

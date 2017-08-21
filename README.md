AVTools
=======

This package provides Audio Video tools, which can be for testing, automation and many other purpose.

Note : All tools are developed for Windows environment and will be extended to Linux over a period

### Prerequisite : Third party tools installation
Here are few installation's(Manual) required before using **Tools/Libraries**

- Install Screen Capture Recorder : https://sourceforge.net/projects/screencapturer/files/
- Install vlc media player : http://www.videolan.org/vlc/ (either 32bit or 64bit)
- Download ffmpeg : https://ffmpeg.org/download.html#build-windows (either 32bit or 64bit)
    uncompress in to `c:\` dir in windows and add in the windows path
- Download Zbar from `http://sourceforge.net/projects/zbar/files/zbar/0.10/zbar-0.10-setup.exe/download`
and install it.
    User should see installation under "C:\Program Files (x86)\ZBar" and also user should see zbar files
     `zbarcam.bat`, `zbarcam.exe`, `zbarimg.exe`, `zlib1.dll` at "C:\Python27".


## image_tools
This package contains multiple modules to create qrcode images/videos and decode those images.

#### create_qrcodes.py
    -   Module to create an qrcode file ( image) and also create video file.

#### crop_images.py
    -   Module to crop image by (left, upper, right, lower) parameters.
        User can pass list of dimensions ( rectangular region) to crop a given images

#### decode_qr_codes.py
    -   Module to decode qrcode.

## ffmpeg_video_tools
#### ffmpegScreenRecorder.py (FFMPEG)
    -   Library to record screen as video using `FFMPEG`

#### ffmpegVideoFrames.py (FFMPEG)
    -   VideoFrames is a Video library to extract video frames (as Images) from
        a given video file. Uses FFMPEG to extract frames.


## vlc_video_tools

#### ExtractAudioFrames.py (VLC)
    -   AudioExtraction is a a/v library required for converting an video file
        in to audio file. Currently this module supports mp3 and wav audio
        codec format.
    -  Tested with VLC Ver2.2.4, 2.2.5 and 3.0.0(Nightly GIT Version)
        Suggested audio codec is wav format as it is lossless and transcoding
        time is less compared to mp3

        Transcodes video and extracs only audio frames,
        As this class Transcodes, this module should support all audio codec
        (with in video) as input.

#### ExtractVideoFrames.py (VLC)
###### Limitation: Video Frames with vlc may freeze and indefinitely and capture same frame. works well with Scene Ratio: ~3-4 (it's VLC limitation)
    -   VideoFrames is a Video library to extract video frames (as Images) from
        a given video file. Uses VLC to extract frames.
        Tested and Works well with VLC 2.2.4 and 3.0.0(GIT Version)


## Utils
#### fileLib.py
    -   Provides method to *get\_file\_checksum*

#### netLib.py
    -   Library containing tools to handle and check network interfaces and IP routing

#### processInfo.py
    -   Checks for the process is running on given machine and returns True/False
    -   Get Process id of the given process name.
#### registry.py
Utility to Interact with Windows Registry to

    - Check if given Registry path exists
    - Get SubKeys in a Key
    - Get all the value and values_names in a give key/Sub-key
    - Get individual  Registry key -> value_name -> value
    - Modify single Registry key -> value_name -> value by value names.

    Hkeys are mapped to short form using a dictionary `mapping`

    Abbreviations:
    hkey - root key ( Handle to registry key)
    key - Main key , which could be software/system configurations key
    sub-key - a key under a main key
    value_name - Name of the parameter under key
    value_data - Data of the value_name


# Examples
Examples on how to imports different libraries and use them
####  -TO DO-
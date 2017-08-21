import pyqrcode
import tempfile
import collections
from os import path, mkdir
import subprocess
import cv2
import platform
from PIL import Image, ImageDraw, ImageFont
from resizeimage import resizeimage

from avtools.ffmpeg_video_tools.ffmpeg import FFMPEG


class CreateQRcode(object):
    """
    Bulk QRCode image creation and video Creation
    """

    def __init__(self, qrcode_prefix_text, count=0, destination=None):
        self.qrcode_prefix_text = qrcode_prefix_text
        self.count = count
        self.qr_code_images = collections.OrderedDict()
        if destination is not None:
            self.dest_folder = destination
            if not path.isdir(self.dest_folder):
                mkdir(self.dest_folder)

        else:
            self.dest_folder = tempfile.mkdtemp()

        if platform.system() == 'Windows':
            self.fonts_path = "C:\\Windows\\Fonts"
        else:
            raise NotImplementedError("Currently Supports for Windows")

    def create_qrcode_images(self):
        """
        Creates a Qrcode files with filename qrcode prefix'ed.
        :return:
        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        filename_prefix = "qrcode"

        get_divison_list = self.__get_image_count_partitions()

        green = Image.new("RGB", (1280, 720), "Green")
        red = Image.new("RGB", (1280, 720), "Red")
        blue = Image.new("RGB", (1280, 720), "Blue")
        grey = Image.new("RGB", (1280, 720), "Grey")

        suffix = [format(item, "05d") for item in xrange(self.count)]
        print suffix
        for i in suffix:
            qr_code_content = self.qrcode_prefix_text + "_" + str(i)
            image_file = filename_prefix + "_" + str(i) + ".png"
            image_count = "image_" + str(i)
            temp_count = int(i)
            abs_path_file = path.join(self.dest_folder, image_file)
            self.qr_code_images[image_count] = abs_path_file

            print "QR code file created : {}".format(abs_path_file)
            big_code = pyqrcode.create(qr_code_content, error='H',
                                       mode='binary')

            big_code.png(abs_path_file, scale=30,
                         module_color=[0, 0, 0, 255],
                         background=[0xff, 0xff, 0xff], quiet_zone=4)

            # Resize height of the image using resize image
            # image_handle = open(abs_path_file, 'r')
            resize_img = Image.open(abs_path_file)
            resize_img = resizeimage.resize_cover(resize_img, [720, 720])
            resize_img.save(abs_path_file, resize_img.format)
            resize_img.close()

            tmp_im = Image.open(abs_path_file)
            # Paste qrcode image on Color image
            if temp_count <= get_divison_list[1]:
                blue.paste(tmp_im, (250, 0))
                blue.save(abs_path_file)

            elif temp_count > get_divison_list[1] and temp_count <= \
                    get_divison_list[2]:
                green.paste(tmp_im, (250, 0))
                green.save(abs_path_file)

            elif temp_count > get_divison_list[2] and temp_count <= \
                    get_divison_list[3]:
                grey.paste(tmp_im, (250, 0))
                grey.save(abs_path_file)

            elif temp_count > get_divison_list[3]:
                red.paste(tmp_im, (250, 0))
                red.save(abs_path_file)

            # Writing text to image_tools
            im = Image.open(abs_path_file)
            draw = ImageDraw.Draw(im)
            # use a font from machine
            calibri_font = path.join(self.fonts_path, "Calibri.ttf")
            fnt = ImageFont.truetype(calibri_font, 20)
            draw.text((340, 10), qr_code_content, font=fnt, fill="maroon")
            im.save(abs_path_file)

        return self.qr_code_images

    def create_qr_code_video(self):
        """
        Creates a H.264 qrcode video with 30 fps
        """
        images = self.create_qrcode_images()

        for key, value in images.items():
            print value
        ff = FFMPEG()
        ffmpeg_path = ff.ffmpeg_path
        image_path = path.join(self.dest_folder, "qrcode_%05d.png")
        video_file = path.join(self.dest_folder, "qrcode_video.mp4")
        cmd_string = """{} -r 30 -f image2 -i {} -vcodec libx264 -y {}""".format(
            ffmpeg_path, image_path, video_file)
        print cmd_string
        p = subprocess.Popen(cmd_string, stdout=subprocess.PIPE, shell=True)
        p.wait()

    def __get_image_count_partitions(self):
        a = divmod(self.count, 4)
        print type(a)
        print a[0]
        a = [0, a[0], a[0] * 2, a[0] * 3]
        return a

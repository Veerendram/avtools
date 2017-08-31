from PIL import Image
from os import path, chdir, getcwd, walk, mkdir
import tempfile


class CropImages(object):
    def __init__(self, image_files_location, crop_file_name_prefix, destination_folder=None):
        """
        Crops multiple images.
        :param image_files_location: Location of all the image file.
        :param crop_file_name_prefix: Prefix for the sliced image file.
        :param destination_folder: Destination folder where sliced images are stored
        """
        # destination location depends on number of slices Images are made in to
        self.image_location = image_files_location
        if destination_folder is not None:
            self.dest_folder = destination_folder
            if not path.isdir(self.dest_folder):
                print "Creating destination director"
                mkdir(self.dest_folder)
        else:
            self.dest_folder = tempfile.mkdtemp()
        self.dest_image_name = crop_file_name_prefix
        self.image_count = 0
        self.image_files = self.get_all_images_as_list()

    def get_all_images_as_list(self):
        """
        Retrives all the image files with full path and turns image files as list
        get all the 'jpg' and 'png' files as list
        :return:
        """
        images = []
        pwd = getcwd()
        if path.isdir(self.image_location):
            print "Got image_tools Folder: {}".format(self.image_location)
        else:
            raise ValueError("Unable to find folder {}".format(self.image_location))

        for fn in next(walk(self.image_location))[2]:
            if fn.endswith('.png') or fn.endswith('.jpg'):
                images.append(path.join(self.image_location, fn))
        if len(images) == 0:
            raise ValueError("Unable to find images in the folder {}".format(self.image_location))
        chdir(pwd)
        return images

    def get_image_count(self):
        """
        Get image count
        :return:
        """
        self.image_count = len(self.image_files)
        return self.image_count

    def slice_image(self, crop_boxs):
        """
        Slices all images in the list ,
        :param crop_boxs: Says the image left, upper, right, lower.
        Ref: http://pillow.readthedocs.io/en/3.4.x/reference/image_tools.html#PIL.image_tools.image_tools.crop
        :return:
        """
        crop_folder_count = 1
        for box in crop_boxs:

            sliced_img_count = 0
            folder = "frame"+str(crop_folder_count)
            cropped_image_folder = path.join(self.dest_folder, folder)
            if not path.isdir(cropped_image_folder):
                print "Creating Cropped image director {}".format(cropped_image_folder)
                mkdir(cropped_image_folder)
            for image in self.image_files:
                print "Cropping image : {} ".format(image)
                cropped_image_file = self.dest_image_name + str(sliced_img_count) + ".png"
                dest = path.join(cropped_image_folder, cropped_image_file)
                print "Cropped image : {}".format(dest)
                img = Image.open(image)
                sliced_img_count = sliced_img_count + 1
                cropimage = img.crop(box)
                cropimage.save(dest)
            crop_folder_count = crop_folder_count+1

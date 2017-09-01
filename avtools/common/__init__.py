from os import path, listdir


def get_image_frames_count(frames_folder):
    """
    Checks for the folder where frames are created and returns created
    frames(images) count.
    NOTE: Testers should make sure they use this method based on the
    video length and frame extraction time.
    :param frames_folder:
    :return: return the status and number of frames available (as list)
    """

    # TODO: May have to implement a timer functionality to wait until frames
    # extraction is complete. --TBD--
    # TODO: Need to check for image files. Add file extension check for
    # jpeg, jpg, png etc..

    num_files = 0
    if path.isdir(frames_folder):
        num_files = len([f for f in listdir(frames_folder)
                         if path.isfile(path.join(frames_folder, f))])
        return num_files

    return num_files

import os
import platform
from main_helper import *

def get_proper_slashes():
    if platform.system() == 'Windows':
        return "\\"
    elif platform.system() == 'Linux':
        return "/"


def get_filename(filepath):
    filep = set_slashes(filepath)
    split_tup = filep.split(get_proper_slashes())
    filename = split_tup[-1]
    filename = filename.split(".")

    return filename[0]


def set_slashes(path):
    if platform.system() == 'Windows':
        path = path.replace("/", "\\")
    elif platform.system() == 'Linux':
        path = path
    else:
        print("Unknown platform")
        return path
    return str(path)

    # TODO DEFINE TYPE OF FILE TO SCAN eg. if zip then unzip first


def get_file_extension(filepath):
    filep = set_slashes(filepath)
    if platform.system() == 'Windows':
        split_tup = filep.split("\\")
    else:
        split_tup = filep.split("/")

    filename = split_tup[-1]
    ext = filename.split(".")
    return ext[1]

# CANT BE TESTED YET ON WINDOWS
def unzip_file(self, file):
    unzip_cmd = "unzip -d " + os.getcwd() + "/unzipped " + file
    try:
        os.system(unzip_cmd)
    except Exception:
        print("Couldn't unzip file" + file)
    finally:
        print("File " + file + " unzipped")

    return True

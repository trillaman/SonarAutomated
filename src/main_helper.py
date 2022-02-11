import os
import platform
import sys

def get_proper_slashes():
    if platform.system() == 'Windows':
        return "\\"
    elif platform.system() == 'Linux':
        return "/"

def check_output_exists(path):
    try:
        report_path = open(path, "w")
    except Exception:
        print("Can't open output file for reporting: " + path)
        sys.exit()

    return report_path

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
def unzip_file(self, project_folder, file_to_unzip):
    unzip_cmd = "unzip -d " + project_folder + " " + file_to_unzip
    try:
        os.system(unzip_cmd)
    except Exception:
        print("Couldn't unzip file" + file_to_unzip + " to " + project_folder)
    finally:
        print("File " + file_to_unzip + " unzipped")

    return True

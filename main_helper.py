import os
import re
import sys
from dotenv import load_dotenv

class MainHelper:
    # TODO DEFINE TYPE OF FILE TO SCAN eg. if zip then unzip first
    def get_file_by_extension(self, file):
        split_tup = os.path.splitext('my_file.txt')
        file_extension = split_tup[1]

        return file_extension

    def unzip_file(self, file):
        unzip_cmd = "unzip -d " + os.getcwd() + "/unzipped " + file
        try:
            os.system(unzip_cmd)
        except Exception:
            print("Couldn't unzip file" + file)
        finally:
            print("File " + file + " unzipped")

        return True

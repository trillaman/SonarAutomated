import os
import sys
from main_helper import *

from dotenv import load_dotenv


class PsalmModule:
    def init_composer(self, p_dir):
        init_comp_cmd = "cd " + p_dir + " && " + "./psalm.phar --init"
        init = False
        try:
            os.system(init_comp_cmd)
            init = True
        except Exception:
            print("Can't init psalm")
            init = False
            sys.exit()

        return init

    def download_psalm_to_project(self, p_dir):
        wget_cmd = "wget https://github.com/vimeo/psalm/releases/latest/download/psalm.phar -O " + str(p_dir)
        downloaded = False
        try:
            os.system(wget_cmd)
            downloaded = True
        except Exception:
            print("Can't download phar to project directory")
            downloaded = False
            sys.exit()

        return downloaded

    def download_composer(self, p_dir):
        download_comp_cmd = "cd " + p_dir + " && " + "composer require --dev psalm/phar"
        dl = False
        try:
            os.system(download_comp_cmd)
            dl = True
        except Exception:
            print("Cannot download composer to project directory")
            sys.exit()

        return dl

    def run_psalm_scan(self, p_dir, p_name):
        rep_file_path = os.path.abspath(p_dir + "/" + p_name + ".txt")
        rep_file = check_output_exists(rep_file_path)

        psalm_cmd = str(os.getenv(
            'PSALM_BIN')) + "/psalm.phar --taint-analysis " + p_dir + " --report=" + rep_file  # Focus on security with --taint-analyis

        try:
            os.system(psalm_cmd)
        except Exception:
            print("Error while running psalm")
            sys.exit()
        finally:
            return True

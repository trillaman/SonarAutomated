import argparse
from sonar_module import SonarModule
from main_helper import MainHelper
import pathlib
import os, sys

def main():
    parser = argparse.ArgumentParser(description='Scan some files')
    parser.add_argument('--file', help='Provide path for file to scan', required=True)
    parser.add_argument('-S', help='Use Sonar scanner', required=False)
    args = parser.parse_args()
    argsdict = vars(args)

    m_helper = MainHelper

    if argsdict['file']  is not None:
        file_to_scan = argsdict['file']

    if argsdict['S']:
        file_extension = m_helper.get_file_by_extension(file_to_scan)
        if file_extension == "zip":
            m_helper.unzip_file(file_to_scan) # TO DO REST

        sonar = SonarModule
        sonar.run_docker_scan(file_to_scan)


if __name__ == "__main__":
    if pathlib.Path(os.getcwd() + "/unzipped").exists() is False:
        try:
            os.system(os.getcwd() + "/unzipped")
            print("Folder unzipped created")
        except Exception:
            print("Can't create folder unzipped in that location " + os.getcwd())
            sys.exit()

    main()


# SHIT THAT LEFT
# re.search(r"(^https://downloads.wordpress.org/plugin/)([\w+.-]+.zip)", url)
# file = open("list_to_scan.txt", "r") # to replace with array
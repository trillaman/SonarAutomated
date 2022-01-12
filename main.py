import argparse
from sonar_module import SonarModule
from main_helper import MainHelper
import pathlib
import os
import sys

m_helper = MainHelper

def init_check():
    path = os.getcwd() + "/unzipped"
    path = m_helper.set_slashes(path)
    if pathlib.Path.exists(path) is False:
        try:
            os.system("mkdir " + path)
            print("Folder unzipped created")
            result = True
        except Exception:
            print("Can't create folder unzipped in that location " + os.getcwd())
            sys.exit()
    return result

def main():
    parser = argparse.ArgumentParser(description='Scan some files')
    parser.add_argument('--file', help='Provide path for file to scan', required=True)
    parser.add_argument('-S', help='Use Sonar scanner', required=False)
    parser.add_argument('--name', help='Give Project Name', required=False)
    project_name = ""
    args = parser.parse_args()
    argsdict = vars(args)

    if argsdict['file']  is not None:
        file_to_scan = argsdict['file']

    if argsdict['name'] is not None:
        project_name = argsdict['name']
    else:
        project_name = m_helper.get_filename(argsdict['file'])

    file_extension = m_helper.get_file_by_extension(file_to_scan)

    if file_extension == "zip":
        m_helper.unzip_file(file_to_scan)  # TO DO REST

    directory_with_project = os.chdir(argsdict['file'])
    print(os.path.abspath(argsdict['file']))


    if argsdict['S']:
        # TODO GET A PATH OF JUST UNZIPPED FILES TO SCAN WITHOUT SCANNING WHOLE UNZIPPED FOLDER
        sonar = SonarModule
        sonar.write_properties_file(directory_with_project, project_name)
        sonar.run_docker_scan(directory_with_project, project_name)

    if file_extension == 'php':




if __name__ == "__main__":
    init_check()
    main()


# SHIT THAT LEFT
# re.search(r"(^https://downloads.wordpress.org/plugin/)([\w+.-]+.zip)", url)
# file = open("list_to_scan.txt", "r") # to replace with array
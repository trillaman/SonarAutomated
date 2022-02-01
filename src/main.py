import argparse
from sonar_module import SonarModule
from main_helper import *
import os
import sys
from dotenv import load_dotenv

load_dotenv()

def init_check():
    path_to_scans = str(os.getenv('WORKING_DIR') + "/scans")
    path_to_scans = set_slashes(path_to_scans)
    result = False

    if not os.path.exists(path_to_scans):
        try:
            os.system("mkdir " + path_to_scans)
            print("Folder for scans created")
            result = True
        except Exception:
            print("Can't create folder 'scans' in that location " + os.getcwd())
            sys.exit()
    else:
        print("Folder scans already exists - omitting")
        result = True

    return result


def main():
    parser = argparse.ArgumentParser(description='Scan some files')
    parser.add_argument('--file', help='File to scan (php or zip)', required=True)
    parser.add_argument('-S', help='Use Sonar scanner', required=False)
    parser.add_argument('-P', help='Use Psalm scanner', required=False)
    parser.add_argument('--name', help='Give Project Name', required=False)

    args = parser.parse_args()
    argsdict = vars(args)
    file_to_scan = ""
    project_name = ""

    if argsdict['file'] is not None:
        file_to_scan = argsdict['file']

    if argsdict['name'] is not None:
        project_name = argsdict['name']
    else:
        project_name = get_filename(argsdict['file'])

    file_extension = get_file_extension(file_to_scan)

    print("Project name: " + project_name)  # DEBUG
    print("File extension: " + file_extension)  # DEBUG

    project_dir = os.getenv('WORKING_DIR') + "/scans/" + project_name

    if not os.path.exists(project_dir):  # Must have for working scan - project folder
        try:
            os.system('mkdir ' + project_dir)
            print("Created folder for project in 'scans'")
        except Exception:
            print("Cannot crate folder for project in 'scans'")

    if file_extension == "zip":
        unzip_file(str(project_dir), file_to_scan)  # UNZIP SHOULD BE TO scans FOLDER
    elif file_extension == 'php':
        os.system('mv ' + file_to_scan + " " + project_dir)

    if argsdict['S'] is not None:
        sonar = SonarModule()  # Creating class instance for Sonar Scanning

        sonar.write_properties_file(project_dir, project_name)  # Creating file with properties for Sonar
        sonar.run_docker_scan(project_dir, project_name)  # Sonar scanning run

    if argsdict['P'] is not None:
        os.system(os.getenv('PSALM_BIN') + "/psalm.phar --taint-analysis " + project_dir)

if __name__ == "__main__":
    init_check()
    main()

# SHIT THAT LEFT
# re.search(r"(^https://downloads.wordpress.org/plugin/)([\w+.-]+.zip)", url)
# file = open("list_to_scan.txt", "r") # to replace with array

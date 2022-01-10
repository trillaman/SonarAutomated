import os
import re
import sys
from dotenv import load_dotenv

class SonarModule:

    def __init__(self):
        load_dotenv()

        self.sonar_url = os.getenv('SONAR_URL')
        self.sudo_pass = os.getenv('SUDO_PASS')
        self.sonar_token = os.getenv('SONAR_TOKEN')
        self.extracted_dir = os.getenv('EXTRACTED_DIR')

    def open_file_with_list(self, list_file_path):
        try:
            file_with_list = open(list_file_path, "r")
        except Exception:
            print("Can't open file with list of folders")
            sys.exit()

        return file_with_list

    # CALLABLE BY FUNCTION
    def write_properties_file(self, p_path, p_name):
        try:
            file_sonar_properties = open(p_path + "/sonar-scanner.properties", "w")  # opening file to write properties for each project
            file_sonar_properties.write("sonar.projectKey=" + p_name + "\n")
            file_sonar_properties.write("sonar.projectName=" + p_name + "\n")
        except Exception:
            print("Error while writing sonar properties file for project: " + p_name)
        finally:
            file_sonar_properties.close()

    def get_project_name(self, line):
        project = re.search(r"^(./wp-plugins-extracted/)([\w+.-]+)", line)
        return project

    def create_properties_for_each(self):
        pfile = self.open_file_with_list("./wp-plugins-extracted/list_of_folders.txt")
        for l in pfile:
            line = l.rstrip("\n")
            project = self.get_project_name(line)   # getting name o project from zip path
            self.write_properties_file(line, str(project[2]))  # writing sonar properties

        pfile.close()

    def run_docker_scan(self, path):
        proj = self.get_project_name(path)
        project_path =  str(self.extracted_dir) + "/" + str(proj[2])
        project_name = str(proj[2])
        sonar_url = self.sonar_url
        sudo_pass = self.sudo_pass
        sonar_token = self.sonar_token
        docker_cmd = "echo " + sudo_pass + " | sudo -s docker run --rm -e SONAR_HOST_URL=" + str(
            sonar_url) + " -e SONAR_LOGIN=" + str(
            sonar_token) + " -v " + project_path + ":/usr/src" + " sonarsource/sonar-scanner-cli -Dsonar.projectName=" + project_name + " -Dsonar.projectKey=" + project_name + " -Dproject.settings=" + project_path + "/sonar-project.properties"  # RIGHT PATH EXECUTED FROM PROJECT FOLDER
        print(docker_cmd)
        os.system(docker_cmd)

    def run(self, file):
        self.run_docker_scan(file)



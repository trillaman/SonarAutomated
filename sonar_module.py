import os
import re

class SonarModule:

        def open_file_with_list(self):
                try:
                        file_with_list = open("./wp-plugins-extracted/list_of_folders.txt", "r")
                except Exception:
                        print("Can't open file")
                return file_with_list
        index = 0

        for l in file_with_list:
                line = l.rstrip("\n")
                project = re.search(r"^(./wp-plugins-extracted/)([\w+.-]+)", line)

                file_sonar_properties = open(line +"/sonar-scanner.properties", "w")
                file_sonar_properties.write("sonar.projectKey=" + str(project[2]) + "\n")
                file_sonar_properties.write("sonar.projectName=" + str(project[2]) + "\n")
                file_sonar_properties.close()

                # Docker part
                project_path = str(os.getenv('EXTRACTED_DIR')) + "wp-plugins-extracted/" + str(project[2])
                project_name = str(project[2])
                sonar_url = os.getenv('SONAR_URL')
                sudo_pass = os.getenv('SUDO_PASS')
                sonar_token = os.getenv('SONAR_TOKEN')

                docker_cmd = "echo "+ sudo_pass + " | sudo -s docker run --rm -e SONAR_HOST_URL=" + str(sonar_url) + " -e SONAR_LOGIN=" + str(sonar_token) + " -v " + project_path + ":/usr/src" + " sonarsource/sonar-scanner-cli -Dsonar.projectName=" + project_name + " -Dsonar.projectKey=" + project_name + " -Dproject.settings=" + project_path + "/sonar-project.properties" # RIGHT PATH EXECUTED FROM PROJECT FOLDER
                print(docker_cmd)
                os.system(docker_cmd)

        file_with_list.close()
#ERRORED 
#sh: 1: Syntax error: "(" unexpected
#sh: 1: Syntax error: "(" unexpected


import os
import re
import time
from dotenv import load_dotenv
import requests

from bs4 import BeautifulSoup

# SCRAPING WORDPRESS PLUGINS PAGE
URL = "https://pl.wordpress.org/plugins/browse/blocks/"
page = requests.get(URL)

plugins = []
plugins_urls = []

class_list = set()

soup = BeautifulSoup( page.content , 'html.parser')

tags = {tag.name for tag in soup.find_all()}


h3 = soup.findAll('h3', {'class': 'entry-title'})
for child_a in h3:
        children = child_a.findChildren("a" , recursive=False)
        print(children[0]['href'])
        plugins_urls.append(children[0]['href'])

# NOW GO THROUGH PLUGINS_URLS TO GET ZIP LINK
# TO DO


load_dotenv()

# STEP 1 - Downloading zips

file = open("list_to_scan.txt", "r")
for line in file:
        try:
                url = line
                #print(url)
                zip_file_name = re.search(r"(^https://downloads.wordpress.org/plugin/)([\w+.-]+.zip)", url)

                #print(zip_file_name[2])
                os.system("mkdir wp-plugins-downloaded")
                os.system("mkdir wp-plugins-extracted")
                curl_cmd = "curl --output ./wp-plugins-downloaded/" + zip_file_name[2] + " --url " + url
                curl_cmd = str(curl_cmd)
                #print(curl_cmd)
                os.system(curl_cmd)
                #time.sleep(3)
                unzip_cmd = "unzip -d ./wp-plugins-extracted/ ./wp-plugins-downloaded/" + zip_file_name[2]
                os.system(unzip_cmd)

        except Exception as ex:
                print(ex)

# STEP 2 - creating sonar-scanner.properties for each folder

os.system("find ./wp-plugins-extracted -maxdepth 1 -type d | grep 'wp-plugins-extracted/' > ./wp-plugins-extracted/list_of_folders.txt")

file_with_list = open("./wp-plugins-extracted/list_of_folders.txt", "r")

for l in file_with_list:
        line = l.rstrip("\n")
        project = re.search(r"^(./wp-plugins-extracted/)([\w+.-]+)", line)

        file_sonar_properties = open(line +"/sonar-scanner.properties", "w")
        file_sonar_properties.write("sonar.projectKey=" + str(project[2]) + "\n")
        file_sonar_properties.write("sonar.projectName=" + str(project[2]) + "\n")
        file_sonar_properties.close()

        # STEP 3 - docker part
        project_path = "./wp-plugins-extracted/" + str(project[2])
        project_name = str(project[2])
        docker_cmd = str("echo os.environ('SUDO_PASS') | sudo -S docker run --rm -e SONAR_HOST_URL='os.environ('SONNAR_URL')' -e SONAR_LOGIN='os.environ('SONNAR_LOGIN')' -v " + project_path + ":/usr/src sonarsource/sonar-scanner-cli -Dsonar.projectBaseDir=" + project_path + " -Dsonar.projectKey=" + project_name)
        os.system(docker_cmd)

# STEP 4 - close files        
file.close()
file_with_list.close()
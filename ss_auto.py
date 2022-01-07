#ERRORED 
#sh: 1: Syntax error: "(" unexpected
#sh: 1: Syntax error: "(" unexpected


import os
import re
import time
from dotenv import load_dotenv
import requests
import time

from bs4 import BeautifulSoup

# SCRAPING WORDPRESS PLUGINS PAGE
URL = "https://pl.wordpress.org/plugins/browse/blocks/"  # main plugins site
page = requests.get(URL)  # we are downloading all html from first page

plugins = []
plugins_urls = []
plugins_zips = []

class_list = set()

soup = BeautifulSoup( page.content , 'html.parser')  # here we are parsing this

tags = {tag.name for tag in soup.find_all()}  # and selecting all tags


h3 = soup.findAll('h3', {'class': 'entry-title'})  # in those tags we are looking for h3 entry title which means name of the plugin

i = 0
for child_a in h3:  # this loop is for getting plugin names and urls to plugin sites
        children = child_a.findChildren("a" , recursive=False)  # here we are looking for link to plugin site which is taken from clickable header
        plugins_urls.append(children[0]['href'])  # and we are adding this to plugin_urls - in this array we will have all link to separated plugins sites
        plugin_name = str(''.join(filter(str.isalnum, child_a.string)))  # here we are removing special characters from title if any
        plugin_name = plugin_name[:10].replace(" ", "")  # and here we are trimming to 10 signs from beginning and removing spaces
        plugins.append(plugin_name)  # here we got clear plugin names for sonnar project
        print(plugins[i])
        print(plugins_urls[i])
        i +=1 


# NOW GO THROUGH PLUGINS_URLS TO GET ZIP LINK

for i in range(len(plugins)):  # for every plugin
        plugin_url = plugins_urls[i]  # we get this url
        plugin_page = requests.get(plugin_url)  # we are downloading page for specific plugin
        soup = BeautifulSoup( plugin_page.content , 'html.parser')  # and parsing this
        #print(soup)
        plugins_zip_url = soup.findAll('a', {'class': 'plugin-download'})  # here we are exrtracting download link to plugin which is leading to zip file
        zip_href = plugins_zip_url[0]['href'] # and here we got clear href
        plugins_zips.append(plugins_zip_url[0]['href'])

        #SONAR PART

        time.sleep(5)

#print(plugins_zips)
# END STEP


load_dotenv()

# SONAR PART
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
'''
# STEP 2 - creating sonar-scanner.properties for each folder
'''
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
'''
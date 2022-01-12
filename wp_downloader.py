import pathlib
import os
import requests
from bs4 import BeautifulSoup
import time
import sys
from main_helper import MainHelper

class WP_Plugin_Downloader:
    URL = "https://pl.wordpress.org/plugins/browse/blocks/"  # main plugins site

    page = requests.get(URL)  # we are downloading all html from first page

    plugins = []  # for storing plugins names
    plugins_urls = []  # for storing plugin urls
    plugins_zips = []  # for storing plugins zip urls

    m_helper = MainHelper

    soup = BeautifulSoup(page.content, 'html.parser')  # here we are parsing this
    tags = {tag.name for tag in soup.find_all()}  # and selecting all tags
    h3 = soup.findAll('h3', {
        'class': 'entry-title'})  # in those tags we are looking for h3 entry title which means name of the plugin

    def __init__(self):
        self.check_wp_folders()

    def check_wp_folders(self):
        path = os.getcwd() + "/wp-plugins-downloaded"
        path = self.m_helper.set_slashes(path)

        if pathlib.Path(path).exists() is False:
            try:
                os.system("mkdir " + path)
                print("Folder wp-plugins-downloaded created")
            except Exception:
                print("Can't create folder wp-plugins-downloaded")
                sys.exit()

        path = os.getcwd() + "/wp-plugins-extracted"
        path = self.m_helper.set_slashes(path)

        if pathlib.Path(path).exists() is False:
            try:
                os.system("mkdir " + path)
                print("Folder wp-plugins-extracted created")
            except Exception:
                print("Can't create folder wp-plugins-extracted")
                sys.exit()

        return True

    def get_plugins_urls(self):
        i = 0
        for child_a in self.h3:  # this loop is for getting plugin names and urls to plugin sites
            children = child_a.findChildren("a",
                                            recursive=False)  # here we are looking for link to plugin site which is taken from clickable header
            self.plugins_urls.append(children[0][
                                         'href'])  # and we are adding this to plugin_urls - in this array we will have all link to separated plugins sites
            plugin_name = str(''.join(
                filter(str.isalnum, child_a.string)))  # here we are removing special characters from title if any
            plugin_name = plugin_name[:10].replace(" ",
                                                   "")  # and here we are trimming to 10 signs from beginning and removing spaces
            self.plugins.append(plugin_name)  # here we got clear plugin names for sonnar project
            print(self.plugins[i])
            print(self.plugins_urls[i])
            i += 1
            time.sleep(1)

        return True

    # NOW GO THROUGH PLUGINS SITES TO GET ZIP LINK
    def get_plugin_zip_urls(self):

        for i in range(len(self.plugins)):  # for every plugin
            plugin_url = self.plugins_urls[i]  # we get this url
            plugin_page = requests.get(plugin_url)  # we are downloading page for specific plugin
            soup = BeautifulSoup(plugin_page.content, 'html.parser')  # and parsing this
            # print(soup)
            plugins_zip_url = soup.findAll('a', {
                'class': 'plugin-download'})  # here we are exrtracting download link to plugin which is leading to zip file
            zip_href = plugins_zip_url[0]['href']  # and here we got clear href
            self.plugins_zips.append(zip_href)
            print(str(zip_href) + " added to array")
            time.sleep(1)

        return True

    # Downloading zips
    def download_wp_plugins(self):
        index = 0

        for el in self.plugins_zips:
            print("Downloading " + self.plugins[index])
            curl_cmd = "curl --output " + self.m_helper.set_slashes( str(os.getcwd()) + "/wp-plugins-downloaded") + self.plugins[index] + " --url " + el
            curl_cmd = self.m_helper.set_slashes(curl_cmd)
            curl_cmd = str(curl_cmd)
            os.system(curl_cmd)
            print("Downloaded " + self.plugins[index])

            print("Unzipping " + self.plugins[index])
            unzip_cmd = "unzip -d ./wp-plugins-extracted/ ./wp-plugins-downloaded/" + self.plugins[index]
            unzip_cmd = self.m_helper.set_slashes(unzip_cmd)
            os.system(unzip_cmd)
            print("Plugin " + self.plugins[index] + " unzipped")

            index += 1

        return True

    def create_list_of_folders(self):
        if os.platform.system() == 'Windows':
            dir_cmd = "dir /a:d /b " + os.getcwd() + "/wp-plugins-extracted" + " > " + os.getcwd()  +"/list_of_folders.txt"
        else:
            dir_cmd = "find ./wp-plugins-extracted -maxdepth 1 -type d | grep 'wp-plugins-extracted/' > ./wp-plugins-extracted/list_of_folders.txt"

        dir_cmd = self.m_helper.set_slashes(dir_cmd)

        try:
            os.system(dir_cmd)
        except Exception:
            print("Failed to create list_of_folders.txt")
            sys.exit()

        return True

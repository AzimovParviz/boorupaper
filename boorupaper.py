import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import ssl
import subprocess
import os
import random
import pathlib
from sys import platform

def os_check():
    if platform == 'linux2':
        print("currently on Linux")
        return 1
    elif platform == 'darwin':
        print("currently on Mac OS")
        return 2


def image_scrape(url, file_type, folder):
        extension = file_type
        filename = folder + extension
        r = requests.get(url)
        with open(filename, 'wb') as outfile:
            outfile.write(r.content)
        setpaper(filename)


def setpaper(file):
        if platform.startswith('darwin'):
            cmd = "osascript -e \'tell application \"Finder\" to set desktop picture to \"" + \
            os.path.dirname(os.path.abspath(__file__)) + "/" + file + "\" as POSIX file" + "\'"
            #example:
            #osascript -e 'tell application "Finder" to set desktop picture to "/path-to-script/wallpaper.png" as POSIX file'
            print(cmd)
            subprocess.call(cmd, shell=True)
            print("success")
        elif platform.startswith('linux'):
            cmd = "gsettings set org.mate.background picture-filename " + \
            os.path.dirname(os.path.abspath(__file__)) + "/" + \
            file
            file + "\""
            print(cmd)
            subprocess.call(cmd, shell=True)
            print("success")
def create_directory(folder):
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
    except OSError:
        print("error creating a directory uwu")


#so no ssl verification errors are given from urlretrieve
ssl._create_default_https_context = ssl._create_unverified_context
#opening the website and getting the direct links to images
ua = UserAgent(verify_ssl=False)
create_directory("content/")
ay = 0
prev_value = 0
url = "https://gelbooru.com/index.php?page=post&s=list&tags=highres+"
tags = input("please write tags separated by comma(not more than 2): ")

if ":" in tags:
    tags.replace(":", "%3a")
if " " in tags:
    tags.replace(" ", "_")
folder = "/content/" + tags
if "," in tags:
    tags = tags.split(',')
    url += tags[0] + '+' + tags[1]
    folder = "content/" + tags[0]
else:
    url += tags
create_directory(folder)
#creating the search link for requested tags
url_page = url + "&pid=" + str(ay)
print(url_page)
response = requests.get(url_page, headers={'User-Agent': ua.chrome})
soup = BeautifulSoup(response.text, 'html.parser')
images = soup.find_all("a", id=True)
#choose a random image from the 1st page
a = images[random.randint(0,len(images))]
post_url = "https:" + a['href']
#requesting the image page
response_post = requests.get(post_url, headers={'User-Agent': ua.chrome})
soup_new = BeautifulSoup(response_post.text, 'html.parser')
images_post = soup_new.find_all("a")
for img in images_post:
    if "Original" in img.text:
        try:
            if '.png' in img['href']:
                extension = '.png'
            elif '.jpg' in img['href'] or '.jpeg' in img['href']:
                extension = '.jpeg'
            elif '.gif' in img['href']:
                extension = '.gif'
            else:
                extension = ".jpg"
            image_scrape(img['href'].replace(".com//", ".com/"), extension, folder)
        except ValueError:
            pass

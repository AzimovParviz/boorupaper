#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import ssl
import subprocess
import os
import random
import pathlib
from pathlib import Path
from sys import platform

# #checks for Linux/MacOS
# def os_check():
#     if platform == 'linux2':
#         print("currently on Linux")
#         return 1
#     elif platform == 'darwin':
#         print("currently on Mac OS")
#         return 2


def image_scrape(url, file_type, folder):
        extension = file_type
        i = 1
        while True:
            if os.path.exists(folder+str(i)+file_type):
                i += 1
            else:
                folder = folder + str(i)
                break
        filename = folder + extension
        r = requests.get(url)
        with open(filename, 'wb') as outfile:
            outfile.write(r.content)
        setpaper(filename)




def setpaper(file):
        if platform.startswith('darwin'):
            cmd = "osascript -e \'tell application \"Finder\" to set desktop picture to \"" + file + "\" as POSIX file" + "\'"
            #example:
            #osascript -e 'tell application "Finder" to set desktop picture to "/path-to-script/wallpaper.png" as POSIX file'
            print(cmd)
            subprocess.call(cmd, shell=True)
            print("success")
        elif platform.startswith('linux'):
            if 'mate' in os.environ.get('DESKTOP_SESSION'):
                cmd = "gsettings set org.mate.background picture-filename " + \
                os.path.dirname(os.path.abspath(__file__)) + "/" + \
                file
                file + "\""
                print(cmd)
                subprocess.call(cmd, shell=True)
                print("success")
            elif 'plasma' in os.environ.get('DESKTOP_SESSION'):
                print("the file is: "+file)
                cmd ="""
                qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript '
    var allDesktops = desktops();
    print (allDesktops);
    for (i=0;i<allDesktops.length;i++) {{
        d = allDesktops[i];
        d.wallpaperPlugin = "org.kde.image";
        d.currentConfigGroup = Array("Wallpaper",
                                     "org.kde.image",
                                     "General");
        d.writeConfig("Image", "file://%s")
    }}
'
                """
                print(cmd % file)
                subprocess.call(cmd % file, shell=True)
                print("success")
            elif 'gnome' in os.environ.get('DESKTOP_SESSION'):
                cmd = "gsettings set org.gnome.desktop.background picture-uri file:/// \"" + \
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
        print("oopsie we made a woopsie wen cweating a diwectory UwU")
        #error message is as horrible as i could think of so there is motivation to not make mistakes
        raise


#so no ssl verification errors are given from urlretrieve
ssl._create_default_https_context = ssl._create_unverified_context
#opening the website and getting the direct links to images
ua = UserAgent(verify_ssl=False)
home = str(Path.home())
print("home directory is: "+home)
create_directory(home+"/.boorupapers/content/")
ay = [0]
prev_value = 0
url = "https://gelbooru.com/index.php?page=post&s=list&tags=highres+rating:safe+"
tags = input("please write tags separated by comma: ")
if ":" in tags:
    tags = tags.replace(":", "%3a")
if " " in tags:
    tags = tags.replace(" ", "_")
folder = home+"/.boorupapers/content/" + tags
j = 0
if "," in tags:
    tags = tags.split(',')
    for items in tags:
        if j<len(tags):
            url += tags[j] + '+'
        else:
            url += tags[j]
        j += 1

    folder = home+"/.boorupapers/content/" + tags[0]
else:
    url += tags
#create_directory(folder)
#creating the search link for requested tags
response = requests.get(url, headers={'User-Agent':ua.chrome})
soup = BeautifulSoup(response.text, 'html.parser')
paginator = soup.find(class_="pagination")
for pages in paginator:
    ay.append(ay[len(ay)-1]+42)
print(ay)
rand_page = ay[random.randint(0,len(ay)-2)]
print(rand_page)
url_page = url + "&pid=" + str(rand_page)
print(url_page)
response = requests.get(url_page, headers={'User-Agent': ua.chrome})
soup = BeautifulSoup(response.text, 'html.parser')
images = soup.find_all("a", id=True)
#choose a random image from the 1st page
a = images[random.randint(0,len(images))-1]
post_url = a['href']
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

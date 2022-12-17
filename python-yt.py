import os
import subprocess
from pytube import YouTube
import random
import requests
import re
import string


#imp functions
default_folder = True  # change to false if want to use custom folder to save 
define_user_res = False

def foldertitle(url):
    try:
        res = requests.get(url)
    except:
        print('no internet')
        return False

    plain_text = res.text

    if 'list=' in url:
        eq = url.rfind('=') + 1
        cPL = url[eq:]

    else:
        print('Incorrect attempt.')
        return False

    return cPL

def link_snatcher(url):
    our_links = []
    try:
        res = requests.get(url)
    except:
        print('no internet')
        return False

    plain_text = res.text

    if 'list=' in url:
        eq = url.rfind('=') + 1
        cPL = url[eq:]
    else:
        print('Incorrect Playlist.')
        return False

    tmp_mat = re.compile(r'watch\?v=\S+?list=' + cPL)
    mat = re.findall(tmp_mat, plain_text)

    for m in mat:
        new_m = m.replace('&amp;', '&')
        work_m = 'https://youtube.com/' + new_m
        if work_m not in our_links:
            our_links.append(work_m)

    return our_links




url = str(input("\nspecify your playlist \n(*must write) url, \n(*must write) folder name,  \n(optional write '-' if not needed) path and \n(optional write '-' if not needed) resolution\n seprated with space and in same order and in single line:\n"))

url, folder_name, path, user_res = url.split()
url = url.strip()
folder_name = folder_name.strip().lower()
user_res = user_res.strip().lower()
path = path.strip()
 
if not user_res or user_res == "-" or user_res == "":
    define_user_res = False
else:
    define_user_res = True
    
if not path or path == "" or path == "-":
    BASE_DIR = os.getcwd()
    base_dir = BASE_DIR
else:
    base_dir = path

    
our_links = link_snatcher(url)

os.chdir(base_dir)
new_folder_name = foldertitle(folder_name)

try:
    os.mkdir(folder_name)
except:
    print('\nfolder already exists')

os.chdir(folder_name)
try:
    SAVEPATH = base_dir + "/" +folder_name
except:
    SAVEPATH = base_dir + '\\' +folder_name

print(f'\n files will be saved to {SAVEPATH}')

x=[]
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        pathh = os.path.join(root, name)

        
        if os.path.getsize(pathh) < 1:
            os.remove(pathh)
        else:
            x.append(str(name))

print('\nconnecting . . .\n')
print()

for index, link in enumerate(our_links):
    try:
        yt = YouTube(link)
        main_title = yt.title
        main_title = main_title + '.mp4'
        main_title = main_title.replace('|', '')
        
    except:
        print('connection problem..unable to fetch video info')
        break

    
    if main_title not in x:
        try:
            if define_user_res:
                vid = yt.streams.filter(progressive=True, file_extension='mp4', res=user_res).first()
            else:
                vid = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                
            print('Downloading(',(index+1),"/",len(link),') . . .  : ' + str(index) + ") " + vid.default_filename + ' and its file size -> ' + str(round(vid.filesize / (1024 * 1024), 2)) + ' MB.')
            vid.download(SAVEPATH, filename=str(index+1) + ") "+vid.default_filename)
            
            print('Video Downloaded')
        except Exception as e:
            print('something is wrong.. please rerun the script: ', end=" ")
            print(e)
    else:
        print(f'\n skipping "{main_title}" video \n')


print(' downloading finished')
print(f'\n all your videos are saved at --> {SAVEPATH}')

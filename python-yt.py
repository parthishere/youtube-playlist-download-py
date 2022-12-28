import os
import subprocess
from pytube import YouTube
import random
import requests
import re
import string
import sys
import time

import tkinter
from tkinter import *
from tkinter import messagebox
import customtkinter

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()
app.geometry("600x680")
app.title("CustomTkinter simple_example.py")

url = ""
path = False
folder_name = ""
user_res = False

def slider_callback(value):
    progressbar_1.set(value)

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

def button_function():
    global url
    global path
    global folder_name
    global user_res
    
    url = url_entry.get()
    folder_name = folder_entry.get()
    if not url or not folder_name:
        messagebox.showwarning(title="Error", message= "Enter URL and Foldername")
    else: 
        our_links = link_snatcher(url)
        
    path = path_entry.get()
    if not path:
        path = False
        BASE_DIR = os.getcwd()
        base_dir = BASE_DIR
    else:
        base_dir = path
    
    user_res = resolution_entry.get()
    if not user_res:
        user_res =False
    frame_1.destroy()
    
    frame_2 = customtkinter.CTkFrame(master=app)
    frame_2.pack(pady=10, padx=20, fill="both", expand=True)
        
    textbox = customtkinter.CTkTextbox(frame_2,  width=600, height=600)
    textbox.place(x=2, y=10)
    
    progressbar_1 = customtkinter.CTkProgressBar(master=frame_2)
    progressbar_1.place(x=300, y=630)
    
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
    textbox.insert(index="0.0",text=f'files will be saved to {SAVEPATH}\n\n')
    x=[]
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            pathh = os.path.join(root, name)

            
            if os.path.getsize(pathh) < 1:
                os.remove(pathh)
            else:
                x.append(str(name))

    print('\nconnecting . . .\n')

    for index, link in enumerate(our_links):
        try:
            yt = YouTube(link)
            main_title = yt.title
            main_title = main_title + '.mp4'
            main_title = main_title.replace('|', '')
            
        except:
            print('connection problem..unable to fetch video info')
            textbox.insert(index="0.0",text=f'connection problem..unable to fetch video info\n\n')
            break

        
        if main_title not in x:
            try:
                if user_res:
                    vid = yt.streams.filter(progressive=True, file_extension='mp4', res=user_res).first()
                else:
                    vid = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                textbox.insert(index="0.0",text=f"Downloading {(index+1)}/{len(link)}... {str(index)}) {vid.default_filename} and its file size -> {str(round(vid.filesize / (1024 * 1024), 2))} MB.\n")
                app.update()
                print('Downloading(',(index+1),"/",len(link),') . . .  : ' + str(index) + ") " + vid.default_filename + ' and its file size -> ' + str(round(vid.filesize / (1024 * 1024), 2)) + ' MB.')
                
                vid.download(SAVEPATH, filename=str(index+1) + ") "+vid.default_filename)
                
                textbox.insert(index="0.0", text="Downloaded\n\n")
                progressbar_1.set((index+1)//len(link))
                app.update()
                print('Video Downloaded \n')
            except Exception as e:
                print('something is wrong.. please rerun the script: ', end=" ")
                print(e)
                textbox.insert(text=f"something is wrong.. please rerun the script: {e}\n\n")
                app.update()
        else:
            print(f'\n skipping "{main_title}" video \n')


    print(' downloading finished')
    textbox.insert(text="downloading finished\n\n")
    app.update()
    time.sleep(2000)
    print(f'all your videos are saved at --> {SAVEPATH}\n\n')
    textbox.insert(text='\n all your videos are saved at --> {SAVEPATH}\n')
    app.update()
    

    
    print("button pressed")
    

frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=10, padx=20, fill="both", expand=True)

# Use CTkButton instead of tkinter Button
label_1 = customtkinter.CTkLabel(frame_1, text="URL")
label_1.place(x=2, y=25)

url_entry = customtkinter.CTkEntry(frame_1, width=300, height=1)
url_entry.place(x=130, y=25)
###############################################################
label_2 = customtkinter.CTkLabel(frame_1, text="Folder Name")
label_2.place(x=2, y=75)

folder_entry = customtkinter.CTkEntry(frame_1)
folder_entry.place(x=130, y=75)
################################################################
label_3 = customtkinter.CTkLabel(frame_1, text="Path to Save" )
label_3.place(x=2, y=125)

path_entry = customtkinter.CTkEntry(frame_1)
path_entry.place(x=130, y=125)
################################################################
label_4 = customtkinter.CTkLabel(frame_1, text="Resolution" )
label_4.place(x=2, y=175)

resolution_entry = customtkinter.CTkEntry(frame_1)
resolution_entry.place(x=130, y=175)
################################################################

button=customtkinter.CTkButton(frame_1, text="Enter", hover_color="#fa2331", command=button_function) 
button.place(x=130, y=210)
app.mainloop()






    

    









# for index, link in enumerate(our_links):
#     try:
#         yt = YouTube(link)
#         main_title = yt.title
#         main_title = main_title + '.mp4'
#         main_title = main_title.replace('|', '')
        
#     except:
#         print('connection problem..unable to fetch video info')
#         break

    
#     if main_title not in x:
#         try:
#             if user_res:
#                 vid = yt.streams.filter(progressive=True, file_extension='mp4', res=user_res).first()
#             else:
#                 vid = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
#             newlabel.configure()
#             print('Downloading(',(index+1),"/",len(link),') . . .  : ' + str(index) + ") " + vid.default_filename + ' and its file size -> ' + str(round(vid.filesize / (1024 * 1024), 2)) + ' MB.')
#             vid.download(SAVEPATH, filename=str(index+1) + ") "+vid.default_filename)
            
#             print('Video Downloaded')
#         except Exception as e:
#             print('something is wrong.. please rerun the script: ', end=" ")
#             print(e)
#     else:
#         print(f'\n skipping "{main_title}" video \n')


# print(' downloading finished')
# print(f'\n all your videos are saved at --> {SAVEPATH}')


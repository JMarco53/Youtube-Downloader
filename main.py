import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk
from tkinter import messagebox
import threading
import multiprocessing
from PIL import ImageTk, Image
import cv2
from time import sleep

from pytube import YouTube
from pytube import Playlist
import os

import pyfiglet
import wget
#********MAIN VAR***********
f= open("frames.txt","w+")
count = 1
g = True

def rename_ytb():
    global filename
    if os.path.exists("YouTube.mp4"):
        print("NAME WAS YOUTUBE")
        for x in range(10):
            os.rename("YouTube.mp4", "{}.mp4".format(ytb.title))
    filename = "{}.mp4".format(ytb.title)
    invalid_char = set('/\:*?"<>|')
    print("BEFORE REPLACING")
    print(filename)
    if any((c in invalid_char) for c in filename):
        filename = filename.replace("/", "")
        filename = filename.replace(":", "")
        filename = filename.replace("*", "")
        filename = filename.replace("?", "")
        filename = filename.replace('"', "")
        filename = filename.replace("<", "")
        filename = filename.replace(">", "")
        filename = filename.replace("|", "")
        print("REPLACE HAVE BEEN MADE")

    print("NO REPLACEMENT NEEDED")
    print(filename)

def get_size():
    global size_list
    global size
    rename_ytb()
    print("GET SIZE IS HERE")
    size_list = []
    size = os.path.getsize(filename)
    size = size/(1024*1024)
    size = round(size, 2)
    size_list.append(size)
    print(size)
def check():
    act_win = AddPage(mp.sub)
    act_win.del_wid()
    if len(res_list) == 1:
        print("YES THERES ONLY ONE")
        act_win.combolist.configure(value=str(res_list[0]))
        act_win.res_title.place(relx=0.33, rely=0.04)
        act_win.combolist.place(relx=0.35, rely=0.3)
        act_win.submit_res.place(relx=0.35, rely=0.7)
    else:
        print("THERES IS TWO RESOLUTION")
        act_win.combolist.configure(value=[str(res_list[0]), str(res_list[-1])])
        act_win.res_title.place(relx=0.33, rely=0.04)
        act_win.combolist.place(relx=0.35, rely=0.3)
        act_win.submit_res.place(relx=0.35, rely=0.7)
def get_title():
    global title_list
    global title
    global tit_check
    title = ytb.title
    if title == "YouTube":
        for x in range(5):
            get_title()
        title = "Could Not Find Tiltle"
    if len(title) > 35:
        title = title[0:35] + "..."
    title_list = []

    title_list.append(title)
    print(title)
    print(title_list) 
def get_resolution():
    global res_list
    global ytb

    res_list = []
    ytb = YouTube(url)
    #print(ytb.streams.filesize())
    get_title()
    for x in ytb.streams.filter(mime_type="video/mp4", progressive="True").all():
        res_list.append(str(x.resolution))
    check()
def download_fuc():
    global count
    global url
    global ytb
    global cmb
    ytb = YouTube(url)
    dwld = ytb.streams.filter(res=str(cmb)).get_highest_resolution().download()
    threading.Thread(target=dwld).start()
#    getImage()  
def getImage():#Fix Bug when renaming image as hqdefault insteadm of maxresdefault 
    global count
    global image_list

    image_list = []
    thumbnailurl= ytb.thumbnail_url
    thumbnail = wget.download(thumbnailurl)
    if os.path.exists("maxresdefault.jpg"):
        if os.path.exists("thumb {}.jpg".format(str(count))):
            print("THUMB ALREADY EXIST")
            os.rename("maxresdefault.jpg", "thumb {}.jpg".format(str(count+1)))#FIX WHEN NAME ALREADY EXIST
        else:
            os.rename("maxresdefault.jpg", "thumb {}.jpg".format(str(count)))
    if os.path.exists("hqdefault.jpg"):
        os.rename("hqdefault.jpg", "thumb {}.jpg".format(str(count)))
        
    image_list.append("thumb {}.jpg".format(str(count)))
    count+=1


class MainPage():
    def insert_frame(self, master):
        PILFile = Image.open(image_list[-1])#.convert("RGBA")
        PILFile = PILFile.resize((110, 62), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(PILFile)
        print("Frame ADDED")

        frame = tk.Frame(self.vid_canvas, height=64, width=785, highlightthickness=0, borderwidth=0)
        frames.append(frame)
        frame.pack(pady=self.h)

        self.vid_title = tk.Label(frames[-1], text=title_list[-1], fg="black", font='Bahnschrift 14')

        self.thumb_image = tk.Label(frames[-1], width=110, height=63, bg="#03adf5", image=img, highlightthickness=2, borderwidth=0)
        self.thumb_image.image = img

    def showAct(self):
        global sub
        self.sub = tk.Toplevel(root)
        self.sub.title("Add Url")
        self.sub.geometry("370x170")
        self.sub.resizable(width=False, height=False)
        act_win = AddPage(self.sub)
        act_win.__init__(self.sub)
        self.plus_but.configure(state="disable")
    def __init__(self, master):
        global HEIGHT
        global WIDTH
        global frames
        global widgets
        global Can1

        self.h = 5
        frames = []
        widgets = []
        HEIGHT = 600
        WIDTH = 800
        self.frame_canvas = tk.Frame(master, height=637, width=WIDTH, highlightthickness=0)
        self.Can1 = tk.Canvas(self.frame_canvas, height=537, width=WIDTH )
        self.vsbar = Scrollbar(self.frame_canvas, orient="vertical", command=self.Can1.yview)
        
        self.vid_canvas = tk.Frame(self.Can1, height=537, width=WIDTH, highlightthickness=0)
        self.vid_canvas.bind("<Configure>", lambda e: self.Can1.configure(scrollregion=self.Can1.bbox("all")))
        self.Can1.create_window((0, 0), window=self.vid_canvas, anchor="nw")
        self.Can1.configure(yscrollcommand=self.vsbar.set)
        
#        for i in range(50):
#            tk.Label(self.vid_canvas, text="Sample scrolling label").pack()
        self.frame_canvas.pack()
        self.Can1.pack(side="left", fill="both", expand=True)
        self.vsbar.pack(side="right", fill="y")

#        self.submit_but = tk.Button(master, text="Submit", bg="#03adf5", borderwidth=0, height=2, width=18, command=lambda : [self.insert_frame(master)])
#        self.submit_but.place(relx=0.45, rely=0.13)

        self.add_sign = tk.PhotoImage(file="add.png") 
#*******NAVIGATION BAR*************************************
        self.nav_bar = tk.Frame(master, bg="#282828", height=70, width=800, highlightthickness=0, borderwidth=0)
        self.nav_bar.place(relx=0, rely=0)

        self.plus_but = tk.Button(self.nav_bar, image=self.add_sign, bg="#03adf5", borderwidth=0, command=lambda : [self.showAct()])
        self.plus_but.place(relx=0.5, rely=0.0)
#*******VIDEO  BAR********************************************


class AddPage:
    def del_wid(self):
        self.url_entry.destroy()
        self.submit_but.destroy()
        self.ytb_url.destroy()
        self.audiON.destroy()
    def check_url(self):
        global url
        global all_good
        global url
        url = self.url_entry.get()
        act_win = AddPage(mp.sub)
        print(url)
        if url == "":
            self.url_entry.delete(first=0,last=1000)
            messagebox.showinfo("Error", "The url can't be blank!")
            
            act_win.__init__(mp.sub)
        else:
            try:
                self.del_wid()
                self.submit_res.place(relx=0.35, rely=0.7)
                get_resolution()
                
            except:
                print("NOT A VALID LINK")
                self.url_entry.delete(first=0,last=1000)
                for x in range(15):
                    act_win.check_url()
#                messagebox.showinfo("Error", "The url is invalid")
    def place_wid(self):
        global  cmb
        mp.insert_frame(root)
        cmb = self.combolist.get()
        print(cmb)
        mp.vid_title.place(relx=0.16, rely=0.3)
        mp.thumb_image.place(relx=0.005, rely=0)
        mp.plus_but.configure(state="normal")
    def submit(self):
        global g
        getImage()
        if g:
            print(g)
            mp.insert_frame(root)
            g = False
        print(ytb.title)
 #       mp.vid_title.configure(text=ytb.title)
        threading.Thread(target=self.place_wid()).start() 
        mp.sub.destroy()
        download_fuc() #Doit ameliorer: Download effectuer avant apparition du titre
        if os.path.exists("YouTube.mp4"):
            print("NAME WAS YOUTUBE")
            for x in range(15):
                os.rename("YouTube.mp4", "{}.mp4".format(ytb.title))
        #get_size()
        #mp.sizeLab = tk.Label(frames[-1], text=str(size_list[-1]) + "MB", fg="black", font='Bahnschrift 14')
        #mp.sizeLab.place(relx=0.6, rely=0.3)
    def see(self):
        print(self.CheckVar1.get())
    def __init__(self, master):
        self.CheckVar1 = tk.StringVar()
        self.current_table = tk.StringVar()

        self.add_win = tk.Frame(master, height=170, width=370, bg="#282828", borderwidth = 0)
        self.add_win.place(relx=0, rely=0)

        self.ytb_url = tk.Label(self.add_win, text="Enter Youtube Url", bg="#282828", fg="white", font='Bahnschrift 14')
        self.ytb_url.place(relx=0.35, rely=0.04)

        self.url_entry = tk.Entry(self.add_win, insertbackground="black", font="Calibri 12", bg="white", fg="black", width=42, borderwidth=0)
        self.url_entry.place(relx=0.05, rely=0.3)

        self.audiON = tk.Checkbutton(self.add_win, text = "Audio Only", bg="#03adf5", fg="white", variable=self.CheckVar1, onvalue = "yes", offvalue = "no", height=1, width = 10, command=lambda : [self.see()])
        self.audiON.place(relx=0.4, rely=0.5)
        print(self.CheckVar1.get())

        self.submit_but = tk.Button(self.add_win, text="Submit", bg="#03adf5", borderwidth=0, height=2, width=18, command=lambda : threading.Thread(target=self.check_url()).start())
                                                                                                                                                                    
        self.submit_but.place(relx=0.35, rely=0.7)#Peut surement ameliorer pour pas lag
        
        self.submit_res = tk.Button(self.add_win, text="Submit", bg="#03adf5", borderwidth=0, height=2, width=18, command=lambda : threading.Thread(target=self.submit()).start())

        self.res_title = tk.Label(self.add_win, text="Choose resolution", bg="#282828", fg="white", font='Bahnschrift 14')
        self.combolist = ttk.Combobox(self.add_win, 
                            values=[
                                    "", 
                                    "",
                                    "",
                                    ""])
        self.combolist.bind("<<>ComboboxSelected>")
        
#*****************************************************
root = tk.Tk()
root.resizable(width=False, height=False)




mp = MainPage(root)

root.mainloop()
from handler.frame_handler import Framework as fw
from time import sleep
from tkinter import messagebox as msgbox
from subprocess import call
from PIL import ImageTk
from os.path import join
import tkinter as tki
import cv2

class Object_box():
    def __init__(self):
        self.exe = tki.Tk()

    def create_instance(self, title, mins, maxs, resize):
        self.exe.title(title)
        if mins != 0 and maxs != 0:
            self.exe.minsize(mins, maxs)
            self.exe.maxsize(mins, maxs)
        if resize == False:
            self.exe.resizable(0,0)
        return self.exe

class Reply_box():
    def __init__(self, reply):
        self.reply = reply

    def showerr(self):
        msgbox.showerror(title="Error", message=self.reply)

    def showinfo(self):
        msgbox.showinfo(title="Reply", message=self.reply)

class Template():
    def __init__(self, main):
        self.master = main

    def status_bar(self, report):
        self.status = tki.Label(self.master, text=report, width=20, relief=tki.GROOVE, anchor="w")
        self.status.pack(side = tki.BOTTOM, fill = tki.X)
        sleep(3)

    def frame_ctrl(self, border):
        self.frames = tki.Frame(self.master, relief=tki.RIDGE, borderwidth=border)
        return self.frames

    def icon_button(self, path, cmd):
        self.icon = tki.PhotoImage(path)
        self.button = tki.Button(self.master, image=self.icon, width=50, height=50, relief=tki.RAISED, command=cmd)
        return self.button
    
    def text_button(self, text, cmd):
        self.text = text
        self.button = tki.Button(self.master, text=self.text, width=30, height=3, relief=tki.RAISED, command=cmd) 
        return self.button

    def entry_bar(self, var):
        self.var = var
        self.entry = tki.Entry(self.master, width=30, textvariable=self.var)
        return self.entry

    def label_bar(self, text, bg):
        self.text = text
        self.bg = bg
        self.label = tki.Label(self.master, width=20, height=2, text=self.text, bg=self.bg)
        return self.label

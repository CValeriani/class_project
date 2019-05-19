from handler.gui_handler import Object_box as create_obj
from handler.gui_handler import Reply_box as reply
from handler.gui_handler import Template
from subprocess import call
from PIL import ImageTk
import threading as thr
from os.path import join
import tkinter as tki

def show_menu():
    submenu = create_obj().create_instance("OnLooker Menu", 400, 500, resize=False)

    # Creating framework for menu
    container = Template(submenu).frame_ctrl(2)
    container.pack(fill=tki.BOTH, expand=1)
    container.config(background="#993399")
    # Title Section
    title = tki.Label(container, text="OnLooker Console", height=2, bg="#DF9FDF")
    title.pack(side=tki.TOP, fill=tki.X)
    # Menu Background
    display = ImageTk.PhotoImage(file=join("handler", "assets", "menu_bg.png"))
    bground = tki.Label(container, image=display)
    bground.pack(side=tki.TOP, fill=tki.BOTH, expand=1)
    # Menu Section
    newstream = Template(bground).text_button(text="Add new camera", cmd=input_newdevice)
    models = Template(bground).text_button(text="Load Data", cmd=load_model)
    train = Template(bground).text_button(text="Create Models", cmd=train_model)    
    cancel = Template(bground).text_button(text="Close menu", cmd=submenu.destroy)

    newstream.pack(side=tki.TOP, pady=4)
    models.pack(side=tki.TOP, pady=4)
    train.pack(side=tki.TOP, pady=4)
    cancel.pack(side=tki.BOTTOM, pady=4)
    submenu.mainloop()

def input_newdevice():
    gui = create_obj().create_instance("Insert new Camera", 0, 0, resize=False)
    input1 = tki.StringVar(gui)
    input2 = tki.StringVar(gui)

    typelabel = Template(gui).label_bar(text="Insert type", bg="#FF00FF")
    buff1 = Template(gui).entry_bar(var=input1)
    camlabel = Template(gui).label_bar(text="Insert camera device", bg="#FF00FF")
    buff2 = Template(gui).entry_bar(var=input2)
    helps = Template(gui).text_button(text="Helps", cmd=show_vidhelp)
    submit = Template(gui).text_button(text="Connect", cmd=lambda:open_vid(input1.get(), input2.get()))
        
    typelabel.grid(row=0, column=0, sticky="news")
    buff1.grid(row=0, column=1, sticky="news")
    camlabel.grid(row=1, column=0, sticky="news")
    buff2.grid(row=1, column=1, sticky="news")
    helps.grid(row=2, column=0, sticky="news")
    submit.grid(row=2, column=1, sticky="news")
    gui.mainloop()

def show_vidhelp():
    helps = create_obj().create_instance("Help", 0, 0, resize=False)
    helps.resizable(0,0)
    header1 = Template(helps).label_bar(text="Type", bg="#FF00FF")
    header2 = Template(helps).label_bar(text="Camera devices", bg="#FF00FF")
    helps1 = Template(helps).label_bar(text="local", bg="#FF00FF")
    helps1a= Template(helps).label_bar(text="webcam", bg="#FF00FF")
    helps1b = Template(helps).label_bar(text="device1", bg="#FF00FF")
    helps1c = Template(helps).label_bar(text="device2", bg="#FF00FF")
    helps2x = Template(helps).label_bar(text="http", bg="#FF00FF")
    helps2a = Template(helps).label_bar(text="address:port(/...)", bg="#FF00FF")
    helps2y = Template(helps).label_bar(text="rtsp", bg="#FF00FF")
    helps2b = Template(helps).label_bar(text="address", bg="#FF00FF")
    helps3x= Template(helps).label_bar(text="xiaomi", bg="#FF00FF")
    helps3a = Template(helps).label_bar(text="address:port", bg="#FF00FF")
    close = Template(helps).text_button(text="Close", cmd=helps.destroy)

    header1.grid(row=0, column=0, sticky="news")
    header2.grid(row=0, column=1, sticky="news")
    helps1.grid(row=1, column=0, sticky="news")
    helps1a.grid(row=1, column=1, sticky="news")
    helps1b.grid(row=2, column=1, sticky="news")
    helps1c.grid(row=3, column=1, sticky="news")
    helps2x.grid(row=4, column=0, sticky="news")
    helps2a.grid(row=4, column=1, sticky="news")
    helps2y.grid(row=5, column=0, sticky="news")
    helps2b.grid(row=5, column=1, sticky="news")
    helps3x.grid(row=6, column=0, sticky="news")
    helps3a.grid(row=6, column=1, sticky="news")
    close.grid(row=7, column=1, sticky="news")
    helps.mainloop()

def call_stream(method, camera):
    try:
        check = call(["python", "vidstream.py", "-m", method, "-c", camera])

        if check: reply("Successful!").showinfo()
        else: reply("Camera has been shutdown").showinfo()
    except: reply("Something went haywire when trying to fetch camera's feed").showerr()

def open_vid(method, camera):
    feeds = thr.Thread(target=call_stream, args=(method, camera,))
    feeds.start()

def load_model():
    try:
        call(["python", "Tfm_load.py"])
        reply("Successful!").showinfo()
    except: reply("Something went haywire when trying to call the program").showerr()

def train_model():
    try:
        call(["python", "train_model.py"])
        reply("Successful!").showinfo()
    except: reply("Something went haywire when trying to call the program").showerr()        
# ========================== Program Starts here ==============================

# try: 
show_menu()
# except:
    # reply("The application has been stopped due to unexpected internal error").showerr()
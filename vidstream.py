from handler.gui_handler import Reply_box as reply
from handler.xiaomi_handler import XiaomiCam as micam
from handler.frame_handler import Framework as fw
import tkinter as tki
import argparse as ap
import cv2
import imutils
import sys
import numpy as np

# Add Arguments-parser for parsing CLI arguments
# 1. Create Argument parser
argp = ap.ArgumentParser()
# 2. Setting argument
argp.add_argument("-m", "--method", required = True, help = "Insert method for camera [local | remote]")
argp.add_argument("-c", "--camera", required = True, help = "Insert camera path for video input")
args = vars(argp.parse_args())
#- ---------------------------------------------

argument_int = 0
argument_str = ""

if args['method'] == "local":
    if args['camera'] == "webcam": argument_int = 0
    elif args['camera'] == "device1": argument_int = 1
    elif args['camera'] == "device2": argument_int = 2
else:
    argument_str = args['camera']

if args['method'] == "local": argv = argument_int
elif args['method'] == "http": argv = "http://"+argument_str
elif args['method'] == "rtsp": argv = "rtsp://"+argument_str+"/1"
elif args['method'] == "xiaomi":
    addr, port = argument_str.split(":")
    
try:
    if args['method'] == "xiaomi":
        print("[>>] Trying to connect to xiaomi device...")
        Yicam = micam(addr, port)
        Yicam.vid_stream()
        # Close Stream
        Yicam.vid_close()
    else:
        print("[>>] Trying to connect to", argv+"...")
        open_vid = fw(argv)
        open_vid.analyze_feed()
except:
    reply("The video cannot be opened due to unexpected error...").showinfo()
    sys.exit()
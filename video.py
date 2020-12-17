import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from PIL import Image
import time
import os
from tkinter import StringVar
from ffpyplayer.player import MediaPlayer


class MyVideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        self.audio = MediaPlayer(video_source)
        audio_frame, val = self.audio.get_frame()
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.fps = float(self.vid.get(cv2.CAP_PROP_FPS))

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            return None, None


class App:
    def __init__(self, window, window_title, paths):
        self.photo = None
        self.window = window
        self.window.title(window_title)
        self.paths = paths
        self.cur_path_var = StringVar()
        self.vid = self.findNextVideo()

        self.canvas = tkinter.Canvas(window, width=800, height=600)
        self.canvas.pack()

        self.btn_snapshot = tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        self.btn_nextVid = tkinter.Button(window, text="Next", width=50, command=self.nextVideo)
        self.btn_nextVid.pack(anchor=tkinter.CENTER, expand=True)

        self.btn_CurPath = tkinter.Entry(window, textvariable=self.cur_path_var, width=50)
        self.btn_CurPath.pack(anchor=tkinter.CENTER, expand=True)

        self.delay = int(1000 // self.vid.fps)
        self.update()
        self.window.mainloop()

    def findNextVideo(self):
        nextVideo = None
        while not nextVideo:
            try:
                nextVideo = self.tryFindNextVideo()
                self.delay = int(1000 // self.vid.fps)
            except:
                pass
        return nextVideo

    def tryFindNextVideo(self):
        cur_path = next(self.paths)
        self.cur_path_var.set(cur_path)
        return MyVideoCapture(cur_path)

    def snapshot(self):
        ret, frame = self.vid.get_frame()
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def nextVideo(self):
        self.vid = self.findNextVideo()

    def update(self):
        ret, frame = self.vid.get_frame()
        if ret:
            image = PIL.Image.fromarray(frame)
            (w, h) = image.size
            if w > h:
                w, h = (800, 800 * h // w)
                image = image.resize((w, h), Image.ANTIALIAS)
                self.photo = PIL.ImageTk.PhotoImage(image=image)
                self.canvas.create_image(0, (600 - h)/2, image=self.photo, anchor=tkinter.NW)
            else:
                w, h = (600 * w // h, 600)
                image = image.resize((w, h), Image.ANTIALIAS)
                self.photo = PIL.ImageTk.PhotoImage(image=image)
                self.canvas.create_image((800 - w)/2, 0, image=self.photo, anchor=tkinter.NW)
        else:
            self.vid = self.findNextVideo()
        self.window.after(self.delay, self.update)


def walk(path):
    for holder, folders, files in os.walk(path):
        for file in files:
            yield os.path.join(holder, file)


App(tkinter.Tk(), "Tkinter and OpenCV", walk("D:\\NSFW\\vids"))

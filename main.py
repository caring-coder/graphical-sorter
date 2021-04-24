import tkinter
import PIL.Image, PIL.ImageTk
from PIL import Image
import time
import os
from tkinter import StringVar
from ffpyplayer.player import MediaPlayer
from ffpyplayer.pic import Image


class App:
    def __init__(self, window, window_title, paths):
        self.photo = None
        self.window = window
        self.window.title(window_title)
        self.paths = paths
        self.cur_path_var = StringVar()
        self.vid = self.find_next_video()

        self.canvas = tkinter.Canvas(window, width=800, height=600)
        self.canvas.pack()

        self.btn_nextVid = tkinter.Button(window, text="Next", width=50, command=self.next_video)
        self.btn_nextVid.pack(anchor=tkinter.CENTER, expand=True)

        self.btn_CurPath = tkinter.Entry(window, textvariable=self.cur_path_var, width=50)
        self.btn_CurPath.pack(anchor=tkinter.CENTER, expand=True)

        self.update()
        self.window.mainloop()

    def find_next_video(self):
        next_video = None
        while not next_video:
            try:
                next_video = self.try_find_next_video()
            except Exception as e:
                print(e)
        return next_video

    def try_find_next_video(self):
        cur_path = next(self.paths)
        self.cur_path_var.set(cur_path)
        return MediaPlayer(cur_path)

    def next_video(self):
        self.vid = self.find_next_video()

    def update(self):
        frame, val = self.vid.get_frame()
        time.sleep(val/1000)
        if frame is not None:
            image, timestamp = frame
            image = PIL.Image.fromarray(image.to_bytearray()[0])
            w, h = image.get_size()
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
            self.vid = self.find_next_video()
        self.window.after(1, self.update)


def walk(path):
    for holder, folders, files in os.walk(path):
        for file in files:
            yield os.path.join(holder, file)


App(tkinter.Tk(), "Tkinter and OpenCV", walk("D:\\NSFW\\vids"))

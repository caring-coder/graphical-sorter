import os
from sys import path

import pyglet
from pyglet.media import MediaDecodeException
from pyglet.media.codecs.ffmpeg import FFmpegSource
from pyglet.media.codecs.wave import WAVEDecodeException

# os.environ["PATH"] += "C:/apps/ffmpeg-4.3.1-2020-11-19-full_build-shared/bin"

filename = None

if pyglet.media.have_ffmpeg():
    print("have ffmpeg")
else:
    print("no ffmpeg")

# vidPath = 'D:\\Vidéos\\python-jumpstart-course-intro-video.mp4'
window = pyglet.window.Window()
player = pyglet.media.Player()
source = pyglet.media.StreamingSource()
# MediaLoad = pyglet.media.load(vidPath)

def walk(path):
    for holder, folders, files in os.walk(path):
        for file in files:
            yield os.path.join(holder, file)

walker = walk("D:\\NSFW\\vids\\tocheck")

# player.play()


def get_video_size(width, height, sample_aspect):
    if sample_aspect < 1.:
        return width * sample_aspect, height
    elif sample_aspect > 1.:
        return width, height / sample_aspect
    else:
        return width, height

@window.event
def on_draw():
    if player.source and player.source.video_format:
        w_width, w_height = window.get_size()
        s_width, s_height = get_video_size(player.source.video_format.width, player.source.video_format.height, player.source.video_format.sample_aspect)
        player.get_texture().blit(0, 0, width=s_width, height=s_height)

@window.event
def on_key_press(symbol, modifiers):
    global filename
    if symbol == pyglet.window.key.A:
        player.pause()
    elif symbol == pyglet.window.key.Z:
        player.play()
    elif symbol == pyglet.window.key.RIGHT:
        filename = next(walker)
        player.queue(pyglet.media.load(filename))
        player.play()
    elif symbol == pyglet.window.key.K:
        next_filename = next(walker)
        player.queue(pyglet.media.load(next_filename))
        player.next_source()
        os.mkdir(os.path.join(os.path.dirname(filename), "keep"))
        os.replace(filename, os.path.join(os.path.dirname(filename), "keep", os.path.basename(filename)))
        filename = next_filename



pyglet.app.run()

import os
import pyglet


def walk(path):
    for holder, folders, files in os.walk(path):
        for file in files:
            yield os.path.join(holder, file)


window = pyglet.window.Window()


@window.event
def on_draw():
    if player.source and player.source.video_format:
        player.get_texture().blit(0, 0)


vids = walk("D:\\NSFW\\vids")

player = pyglet.media.Player()


@player.event
def on_player_next_source():
    for path in vids:
        try:
            media_load = pyglet.media.load(path)
            player.queue(media_load)
            return
        except Exception as e:
            print(path + " couldn't be loaded")


path = next(vids)
try:
    media_load = pyglet.media.load(path)
    player.queue(media_load)
except Exception as e:
    print(path + " couldn't be loaded")

player.play()
player.event()
pyglet.app.run()











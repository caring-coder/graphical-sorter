import os
from os import path

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

from datetime import timedelta


def walk(path):
    for holder, folders, files in os.walk(path):
        for file in files:
            yield os.path.join(holder, file)


root_path = "D:\\NSFW"
paths = walk(path.join(root_path, "vids"))
del_path = path.join(root_path, "vids", "del")
keep_path = path.join(root_path, "vids", "keep")
meme_path = path.join(root_path, "vids", "meme")
cur_path = next(paths)
cur_duration = 0
cur_position = 0

if __name__ == '__main__':
    app = QApplication([])
    main_window = QMainWindow()
    main_window.setGeometry(200, 200, 700, 500)
    main_window.show()
    player = QMediaPlayer()

    def duration_update(duration):
        global cur_duration, cur_path, cur_position
        cur_duration = player.duration()
        main_window.setWindowTitle(cur_path + " " + str(timedelta(seconds=cur_position//1000)) + "/" + str(timedelta(seconds=cur_duration//1000)))

    def position_update(position):
        global cur_duration, cur_path, cur_position
        cur_position = player.position()
        main_window.setWindowTitle(cur_path + " " + str(timedelta(seconds=cur_position//1000)) + "/" + str(timedelta(seconds=cur_duration//1000)))

    player.durationChanged.connect(duration_update)
    player.positionChanged.connect(position_update)
    wgt_video = QVideoWidget()  # Video display widget
    wgt_video.show()
    main_window.setCentralWidget(wgt_video)
    player.setVideoOutput(wgt_video)  # widget for video output
    q_media_content = QMediaContent(QUrl("file:///"+cur_path))
    player.setMedia(q_media_content)  # Select video file


    def on_key_press(event):
        global cur_path
        key = event.key()
        if key == Qt.Key_Right:
            player.stop()
            source_path = cur_path
            cur_path = next(paths)
            content = QMediaContent(QUrl("file:///" + cur_path))
            player.setMedia(content)
            player.play()
        elif key == Qt.Key_Delete:
            player.stop()
            source_path = cur_path
            cur_path = next(paths)
            content = QMediaContent(QUrl("file:///" + cur_path))
            player.setMedia(content)
            player.play()
            source_basename = path.basename(source_path)
            target_path = path.join(del_path, source_basename)
            os.rename(source_path, target_path)
        elif key == Qt.Key_K:
            player.stop()
            source_path = cur_path
            cur_path = next(paths)
            content = QMediaContent(QUrl("file:///" + cur_path))
            player.setMedia(content)
            player.play()
            source_basename = path.basename(source_path)
            target_path = path.join(keep_path, source_basename)
            os.rename(source_path, target_path)
        elif key == Qt.Key_M:
            player.stop()
            source_path = cur_path
            cur_path = next(paths)
            content = QMediaContent(QUrl("file:///" + cur_path))
            player.setMedia(content)
            player.play()
            source_basename = path.basename(source_path)
            target_path = path.join(meme_path, source_basename)
            os.rename(source_path, target_path)


    main_window.keyPressEvent = on_key_press
    main_window.setWindowTitle(cur_path)
    player.play()
    app.setStyle("Fusion")
    app.exec_()

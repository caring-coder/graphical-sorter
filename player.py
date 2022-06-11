import os
from os import path

from PyQt5.QtCore import QUrl, Qt, QRect
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

from datetime import timedelta


def walk(dir_path):
    for holder, folders, files in os.walk(dir_path):
        for file in files:
            yield path.join(holder, file)


def move_file_to_dir(source_path, target_dir):
    source_basename = path.basename(source_path)
    target_path = path.join(target_dir, source_basename)
    os.makedirs(target_dir, exist_ok=True)
    try:
        os.rename(source_path, target_path)
    except FileNotFoundError as err:
        print(err)


class GraphicalSorterWindow(QMainWindow):

    def __init__(self, left, top, width, height, root):
        super().__init__()
        self.shortcut_folders = dict()
        self.root = root
        self.index = 1
        self.playlist = filter(lambda name: path.isfile(path.join(self.root, name)), iter(os.listdir(self.root)))
        self.current_video = next(self.playlist)
        self.cur_duration = 0
        self.cur_position = 0

        self.setGeometry(QRect(left, top, width, height))

        self.video_widget = QVideoWidget()
        self.setCentralWidget(self.video_widget)

        self.player = QMediaPlayer()
        self.player.durationChanged.connect(self.duration_updater())
        self.player.positionChanged.connect(self.position_updater())
        self.player.setVideoOutput(self.video_widget)
        q_media_content = QMediaContent(QUrl("file:///" + path.join(self.root, self.current_video)))
        self.player.setMedia(q_media_content)  # Select video file

        self.show()
        self.video_widget.show()
        self.player.play()

    def title_update(self):
        position_timestamp = str(timedelta(seconds=self.cur_position // 1000))
        duration_timestamp = str(timedelta(seconds=self.cur_duration // 1000))
        new_window_title = "{0} {1}/{2} {3}/{4}".format(self.current_video, position_timestamp, duration_timestamp, self.index, len(os.listdir(self.root)) + 1)
        self.setWindowTitle(new_window_title)

    def duration_updater(self):
        def duration_update(duration):
            self.cur_duration = duration
            self.title_update()
        return duration_update

    def position_updater(self):
        def position_update(position):
            self.cur_position = position
            self.title_update()
        return position_update

    def keyPressEvent(self, event):
        key = event.key()
        if key in self.shortcut_folders:
            source_path = path.join(self.root, self.current_video)
            self.next_media()
            move_file_to_dir(source_path, self.shortcut_folders[key])
            self.index -= 1
        elif key == Qt.Key_Right:
            self.next_media()
        elif key == Qt.Key_O:
            source_path = path.join(self.root, self.current_video)
            os.system('"{0}"'.format(source_path))

    def next_media(self):
        self.player.stop()
        try:
            self.current_video = next(self.playlist)
            self.index += 1
        except StopIteration:
            self.playlist = filter(lambda name: path.isfile(path.join(self.root, name)), iter(os.listdir(self.root)))
            self.current_video = next(self.playlist)
            self.index = 1
        content = QMediaContent(QUrl("file:///" + path.join(self.root, self.current_video)))
        self.player.setMedia(content)
        self.player.play()

    def add_shortcut(self, folder_path, qt_key_ref):
        self.shortcut_folders[qt_key_ref] = folder_path


if __name__ == '__main__':
    root_folder = "D:\\Drive\\work\\nsfw\\vids"
    del_folder = path.join(root_folder, "del")
    keep_folder = path.join(root_folder, "keep")
    meme_folder = path.join(root_folder, "meme")

    app = QApplication([])

    main_window = GraphicalSorterWindow(200, 200, 700, 500, root_folder)
    main_window.add_shortcut(del_folder, Qt.Key_Delete)
    main_window.add_shortcut(keep_folder, Qt.Key_K)
    main_window.add_shortcut(meme_folder, Qt.Key_M)

    app.setActiveWindow(main_window)
    app.setStyle("Fusion")
    app.exec_()

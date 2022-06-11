from os import path, listdir, rename, makedirs, system

from PyQt5.QtCore import QUrl, Qt, QRect
from PyQt5.QtWidgets import QApplication, QMainWindow, QLayout, QStackedLayout, QHBoxLayout, QLabel, QPushButton, \
    QGridLayout, QWidget, QVBoxLayout
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
    makedirs(target_dir, exist_ok=True)
    try:
        rename(source_path, target_path)
    except FileNotFoundError as err:
        print(err)
    return path.getsize(target_dir)


def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"

class GraphicalSorterWindow(QMainWindow):

    def __init__(self, left, top, width, height, root):
        super().__init__()
        self.shortcut_folders = dict()
        self.shortcut_labels = dict()
        self.shortcut_counters = dict()
        self.root = root
        self.index = 1
        self.playlist = filter(lambda name: path.isfile(path.join(self.root, name)), iter(listdir(self.root)))
        self.current_video = next(self.playlist)
        self.cur_duration = 0
        self.cur_position = 0

        self.setGeometry(QRect(left, top, width, height))
        self.video_widget = QVideoWidget()

        self.h_layout = QHBoxLayout()
        self.h_layout.setContentsMargins(0, 0, 0, 0)

        grid = QVBoxLayout()
        grid.addWidget(self.video_widget, stretch=1)
        grid.addLayout(self.h_layout)

        self_widget = QWidget(self)
        self_widget.setLayout(grid)
        self.setCentralWidget(self_widget)

        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
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
        nb_files = len(listdir(self.root))
        new_window_title = f"{self.current_video} {position_timestamp}/{duration_timestamp} {self.index}/{nb_files}"
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
            moved_size = move_file_to_dir(source_path, self.shortcut_folders[key])
            self.shortcut_counters[key] += moved_size
            self.shortcut_labels[key].setText(path.basename(self.shortcut_folders[key]) + ": " + get_size_format(self.shortcut_counters[key]))
            self.index -= 1
        elif key == Qt.Key_Right:
            self.next_media()
        elif key == Qt.Key_O:
            source_path = path.join(self.root, self.current_video)
            system('"{0}"'.format(source_path))

    def next_media(self):
        self.player.stop()
        try:
            self.current_video = next(self.playlist)
            self.index += 1
        except StopIteration:
            self.playlist = filter(lambda name: path.isfile(path.join(self.root, name)), iter(listdir(self.root)))
            self.current_video = next(self.playlist)
            self.index = 1
        content = QMediaContent(QUrl("file:///" + path.join(self.root, self.current_video)))
        self.player.setMedia(content)
        self.player.play()

    def add_shortcut(self, folder_path, qt_key_ref):
        self.shortcut_folders[qt_key_ref] = folder_path
        self.shortcut_counters[qt_key_ref] = 0
        self.shortcut_labels[qt_key_ref] = QLabel(path.basename(folder_path) + ": " + str(0))
        self.h_layout.addWidget(self.shortcut_labels[qt_key_ref])


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

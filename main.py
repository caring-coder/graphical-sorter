import os
from PIL import Image


def rate(path):
    try:
        with Image.open(path) as image:
            print(path)
    except OSError:
        pass


def walk(path):
    for holder, folders, files in os.walk(path):
        for file in files:
            yield os.path.join(holder, file)


if __name__ == '__main__':
    for path in walk("D:\\NSFW\\vids"):
        print(path)




import ffmpeg
import os

os.makedirs('thumbs', exist_ok=True)

in_filename = 'D:\\tests\\sources\\4994351.webm'

ffmpeg\
    .input(in_filename)\
    .filter('select', 'gte(n,{})'.format(1))\
    .output('thumbs/img0000000.jpeg', vframes=1)\
    .run(overwrite_output=True)

ffmpeg.input(in_filename)\
    .filter('select', 'gt(scene,{})'.format(0.4))\
    .output('thumbs/img%07d.jpeg', vsync='vfr')\
    .run(overwrite_output=True)


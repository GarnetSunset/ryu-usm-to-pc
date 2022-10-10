import subprocess
from os import makedirs, listdir, remove
from os.path import isfile, join, exists, splitext

import ffmpeg
from PyCriCodecs import USM

path = "R:/Downloads/PS5MovieUpgrade/moviesd"
sofdec2enc = "R:/Documents/Programming/Tools/Sofdec2/sofdec2enc.exe"

for filename in listdir(path):
    fullPath = join(path, filename)
    if isfile(fullPath):
        pathname, extension = splitext(fullPath)
        if not exists(pathname):
            makedirs(pathname)
        usmObj = USM(fullPath)
        usmObj.demux()
        usmObj.extract(pathname)
        if not exists(f'{pathname}/workspace/mov_conv_work/00000.avi'):
            stream = ffmpeg.input(f'{pathname}/workspace/mov_conv_work/00000.ivf')
            stream = ffmpeg.output(stream, f'{pathname}/workspace/mov_conv_work/00000.avi', **{'qscale:v': 0})
            ffmpeg.run(stream)

            audio0 = ffmpeg.input(f'{pathname}/workspace/mov_conv_work/audio0.hca')
            audio0 = ffmpeg.output(audio0, f'{pathname}/workspace/mov_conv_work/audio0.wav', **{'qscale:v': 0})
            ffmpeg.run(audio0)

            audio1 = ffmpeg.input(f'{pathname}/workspace/mov_conv_work/audio1.hca')
            audio1 = ffmpeg.output(audio1, f'{pathname}/workspace/mov_conv_work/audio1.wav', **{'qscale:v': 0})
            ffmpeg.run(audio1)
        if isfile(f'{pathname}/workspace/mov_conv_work/00000.avi') and isfile(
                f'{pathname}/workspace/mov_conv_work/00000.ivf'):
            remove(f'{pathname}/workspace/mov_conv_work/00000.ivf')
            remove(f'{pathname}/workspace/mov_conv_work/audio0.hca')
            remove(f'{pathname}/workspace/mov_conv_work/audio1.hca')
        createUsm = subprocess.run(
            [sofdec2enc, '-gop_closed=on', '-gop_i=1', '-gop_p=4', '-gop_b=2',
             f'-video00="{pathname}\workspace\mov_conv_work\00000.avi"', f'-output="{fullPath}"', '-bitrate=20000000',
             f'-audio00="{pathname}\workspace\mov_conv_work\audio0.wav"',
             f'-audio01="{pathname}/workspace/mov_conv_work/audio1.wav"'])

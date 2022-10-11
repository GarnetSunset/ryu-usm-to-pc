from os import makedirs, listdir, remove, system
from os.path import isfile, join, exists, splitext

import ffmpeg
from PyCriCodecs import USM

path = "R:/Downloads/PS5MovieUpgrade/moviesd"
sofdec2enc = "R:/Documents/Programming/Tools/Sofdec2/sofdec2enc.exe"

for filename in listdir(path):
    fullPath = join(path, filename)
    if isfile(fullPath) and ".bak" in fullPath:
        pathname, extension = splitext(fullPath)
        extractPath = f'{pathname}-extract'
        if not exists(extractPath):
            makedirs(extractPath)
        usmObj = USM(fullPath)
        usmObj.demux()
        usmObj.extract(extractPath)
        if not exists(f'{extractPath}/workspace/mov_conv_work/00000.avi'):
            stream = ffmpeg.input(f'{extractPath}/workspace/mov_conv_work/00000.ivf', **{"hwaccel": "nvdec"})
            stream = ffmpeg.output(stream, f'{extractPath}/workspace/mov_conv_work/00000.avi', **{'qscale:v': 1})
            ffmpeg.run(stream)
            if exists(f'{extractPath}/workspace/mov_conv_work/audio0.hca'):
                system(
                    f'ffmpeg -i {extractPath}/workspace/mov_conv_work/audio0.hca -filter_complex '
                    f'"channelmap=map=FL-FL|FR-FR|FC-BL|LFE-BR|BL-FC|BR-LFE:channel_layout=5.1" '
                    f'{extractPath}/workspace/mov_conv_work/audio0.wav')
            if exists(f'{extractPath}/workspace/mov_conv_work/audio1.hca'):
                system(
                    f'ffmpeg -i {extractPath}/workspace/mov_conv_work/audio1.hca -filter_complex '
                    f'"channelmap=map=FL-FL|FR-FR|FC-BL|LFE-BR|BL-FC|BR-LFE:channel_layout=5.1" '
                    f'{extractPath}/workspace/mov_conv_work/audio1.wav')
        if isfile(f'{extractPath}/workspace/mov_conv_work/00000.avi') and isfile(
                f'{extractPath}/workspace/mov_conv_work/00000.ivf'):
            remove(f'{extractPath}/workspace/mov_conv_work/00000.ivf')
            try:
                remove(f'{extractPath}/workspace/mov_conv_work/audio0.hca')
            except:
                pass
            try:
                remove(f'{extractPath}/workspace/mov_conv_work/audio1.hca')
            except:
                pass
        if isfile(f'{extractPath}/workspace/mov_conv_work/00000.avi') and not isfile(pathname):
            if isfile(f'{extractPath}/workspace/mov_conv_work/audio0.wav'):
                createUsm = system(
                    f'{sofdec2enc} -br_range=0,60000000 -video00=\"{extractPath}/workspace/mov_conv_work/00000.avi\" -output=\"{pathname}\" -audio00=\"{extractPath}/workspace/mov_conv_work/audio0.wav\" -audio01=\"{extractPath}/workspace/mov_conv_work/audio1.wav\"')
            else:
                createUsm = system(
                    f'{sofdec2enc} -br_range=0,60000000 -video00=\"{extractPath}/workspace/mov_conv_work/00000.avi\" -output=\"{pathname}')

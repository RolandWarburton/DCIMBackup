from os import popen
from datetime import datetime
from dateutil import parser
import errno
from shutil import move
from os import listdir, mkdir
from os.path import isfile, join, splitext, realpath, dirname


# requires exiftool library from your package manager
def getDestFilepath(filepath):
    # command returns a json string
    # https://stackoverflow.com/questions/31541489/ffmpeg-get-creation-and-or-modification-date
    command = f"ffprobe -v quiet -select_streams v:0 -show_entries stream_tags=creation_time -of default=noprint_wrappers=1:nokey=1 {filepath}"
    # run the command
    stream = popen(command)
    output = stream.readlines()
    # check there was some data returned
    if not len(output) == 1:
        return datetime.today().strftime('%Y-%m-%d')
    else:
        ts = parser.parse(output[0])
        year = ts.year
        month = f"{ts.month:02d}"
        # return the filepath that this mp4 should belong in
        fp = realpath(f"{base_directory}/{year}/{month}")
        return fp


# directory to read
base_directory = "/run/user/1000/gvfs/smb-share:server=store,share=backup/mobile_photos"

# store files we find here
mp4Files = []

# read every file in the directory
files = [f for f in listdir(base_directory) if isfile(join(base_directory, f))]

# sort .mp4 into an array
for file in files:
    fileParts = splitext(file)
    fileExt = fileParts[1]
    if fileExt == ".mp4":
        mp4Files.append(file)

for file in mp4Files:
    sourceFilepath = realpath(f"{base_directory}/{file}")
    destFilepath = getDestFilepath(sourceFilepath)
    try:
        mkdir(dirname(destFilepath))
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    # then try to move the file
    try:
        # if the file already exists the move command will skip it
        move(sourceFilepath, destFilepath)
        print(destFilepath)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass

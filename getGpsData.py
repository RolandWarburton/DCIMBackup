import json
from os import listdir
from os.path import isfile, join, splitext, realpath
from get_latitude_longitude import get_latitude_longitude


# directory to read
# base_directory = "photos"
base_directory = "/run/user/1000/gvfs/smb-share:server=store,share=backup/mobile_photos"

# store files we find here
jpgFiles = []
mp4Files = []

# results with the filename, lat, and lon
results = []

# read every file in the directory
files = [f for f in listdir(base_directory) if isfile(join(base_directory, f))]

# sort .jpg and .mp4 into their arrays
for file in files:
    fileParts = splitext(file)
    fileExt = fileParts[1]
    if fileExt == ".jpg":
        jpgFiles.append(file)
    if fileExt == ".mp4":
        mp4Files.append(file)

for file in jpgFiles:
    real_path = realpath(f"{base_directory}/{file}")
    # print(f"processing file {real_path}")
    lat_lon = get_latitude_longitude(real_path)
    new_result = {"filename": real_path, **lat_lon}
    results.append(new_result)

results_string = json.dumps(results, indent=4, sort_keys=True)
open("location_data.json", "w").write(results_string)

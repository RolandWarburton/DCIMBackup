from os import popen


# requires exiftool library from your package manager
def get_latitude_longitude(filepath):
    commands = {
        "lat": f"exiftool {filepath} -s -s -s -GPSLatitude",
        "lon": f"exiftool {filepath} -s -s -s -GPSLongitude"
    }
    result = {}
    for key in commands:
        # run the command
        stream = popen(commands[key])
        output = stream.readlines()
        # check if there is at least 1 index in the array. 1 is expected
        if not len(output) == 1:
            print(f"skipping {filepath} no GPS data found")
            result[key] = 0.00
        else:
            # process the output from the command
            output = output[0]
            parsed = output.replace("\'", "").replace("\"", "").split()
            seconds = float(parsed[3])
            minimum = float(parsed[2])
            degrees = float(parsed[0])
            degrees = (((seconds/60) + minimum) / 60) + degrees
            # make South and West directions negative
            if parsed[4] == "S" or parsed[4] == "W":
                degrees = degrees * -1
            result[key] = degrees

    return result

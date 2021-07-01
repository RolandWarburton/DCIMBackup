DIR="/home/roland/mobile_photos"
cd $DIR && \
exiftool -d %Y/%m "-directory<datetimeoriginal" *.jpg


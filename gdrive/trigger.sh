inotifywait -q -m -e close_write --format %e ../../cameraLocations.csv |
while read events; do
  python quickstart.py
done

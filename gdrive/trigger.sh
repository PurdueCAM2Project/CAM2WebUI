while inotifywait -e close_write ../../cameraLocations.csv; do python quickstart.py; done

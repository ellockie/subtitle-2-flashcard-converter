#!/bin/bash
set -e

#python -m utils.fetch_subtitles
python -m utils.fetch_subtitles_ui
#echo "Will launch Docker container"
#docker-compose up # --build  ## now run in the python script
echo "Script finished successfully"

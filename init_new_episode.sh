#!/bin/bash
set -e

python -m utils.fetch_subtitles_ui
docker-compose up # --build

#!/bin/bash
set -e

python ./fetch_subtitles.py
docker-compose up # --build

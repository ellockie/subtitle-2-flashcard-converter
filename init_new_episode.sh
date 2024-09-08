#!/bin/bash
set -e

python -m utils.fetch_subtitles
docker-compose up # --build

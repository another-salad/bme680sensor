#! /bin/bash
cd /home/pi/bme680sensor/
/home/pi/.local/bin/pipenv install
/home/pi/.local/bin/pipenv run python app/main_api.py

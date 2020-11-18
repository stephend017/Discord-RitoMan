#!/bin/bash
# this script should be run in the folder containing the source code
# update source code
git pull

# start venv
source venv/bin/activate

# install new version
pip install . 

# stop any existing versions
pm2 stop ritoman

# delete any existing versions
pm2 delete ritoman

# run the script forever
pm2 start python3.8 discord_ritoman/__main__.py --name ritoman --interpreter python3

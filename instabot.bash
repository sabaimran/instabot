#!/bin/bash

source /home/user/miniconda3/bin/activate # I needed this line to activate conda environment when scheduling a cronjob.
conda init bash
conda activate instabot
python3 /home/user/path/to/this-project/insta-bot/instabot.py --config /home/user/path/to/this-project/insta-bot/sample_config.yml
conda deactivate
# Suntree Inventory Tracker
Inventory tracker built for Suntree United Methodist Church

## Setup
### Requirements
* Python 3
* ZBar


### Setup
1. Install zbar. On Ubuntu/Debian based systems, this can be done with `sudo apt install zbar-tools`.
2. Install dependencies for `cv2`: `sudo apt-get install ffmpeg libsm6 libxext6`
 
### Running
1. Clone this repository
1. Run `pip install -r requirements.txt` from the root directory of the repository.
	1.This only needs to be run the first time you are starting the application.
1. Run `cd sit; python main.py` from the root directory of this repository.
	1. Suntree Inventory Tracker will now be accessible in your browser of choice at `localhost:9263`.

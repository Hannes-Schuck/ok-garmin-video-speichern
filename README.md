# Ok Garmin, Video Speichern

A simple python script that uses speech recognition to save a replay using [gpu-screen-recorder](https://git.dec05eba.com/gpu-screen-recorder/about/) to save video replays on Linux when you say "Ok Garmin, Video speichern" (based on the [meme](https://www.youtube.com/watch?v=O02Q5jMAeBI)).

A similar repository can be found [here](https://github.com/lorberry/ok-garmin-video-speichern) (where even the original sounds are used).

## Setup

Tested on CachyOS (6.17.8-2-cachyos)

### Clone the repository
`git clone https://github.com/Hannes-Schuck/ok-garmin-video-speichern.git`

`cd ok-garmin-video-speichern`

### Download the speech recognition model (hosted locally, takes around 3.1 GB unzipped)
`wget https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip`

`unzip vosk-model-de-0.21.zip`

### Install gpu-screen-recorder
`flatpak install flathub com.dec05eba.gpu_screen_recorder`

### Create a virtual environment
`python -m venv .venv`

`source ./.venv/bin/activate.fish` (when using fish shell)

### Install dependencies

`pip install -r requirements.txt`

### Run the script
`python main.py`


Since the communication between the script and the screen recorder uses signals, there are a few more available under `gpu-screen-recorder --help`

(when installed as flatpak: `/var/lib/flatpak/app/com.dec05eba.gpu_screen_recorder/current/<id>/files/bin/gpu-screen-recorder`)

## Create executable binary

`pip install pyinstaller`

Adjust according to the used versions

`pyinstaller --onefile --add-data "vosk-model-de-0.21:vosk-model-de-0.21" --add-binary ".venv/lib/python3.13/site-packages/vosk/libvosk.so:vosk" main.py`

Executable should be created in `./dist/`

# Copyright Notice
This application includes the Vosk German speech recognition model
"vosk-model-de-0.21", developed by Alpha Cephei Inc.
Licensed under the Apache License, Version 2.0.
https://alphacephei.com/vosk/models
https://www.apache.org/licenses/LICENSE-2.0
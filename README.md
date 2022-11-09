
# Voice-controlled Audio Player
A simple voice user interface for controlling playback of an audio player web app.

## Usage
The following commands are supported:

1. `Hey, player!` - to initiate voice commands
2. `Play` - to play the current song
3. `Pause` - to pause the current song
4. `Rewind` - to play the current song from the beginning
5. `Next` - to switch to the next song
6. `Previous` - to switch to the previous song
7. `Mute` - to mute the volume
8. `Unmute` - to unmute the volume

To command the app, start by saying `Hey, player!` followed by one of the commands listed above.

## Audio Player
An audio player web app was built entirely by [Mark Hillard - https://codepen.io/markhillard/pen/jOOKxM](https://codepen.io/markhillard/pen/jOOKxM) and all credits for this part of the project go to him.

The only part that was added by me is `main.py` for locally hosting the web page.

## Voice Controller
This part of the project is responsible for connecting to the audio player using Selenium and providing a way to control the playback.

## Command Recognition
The core module of the project, where the user's voice is recognized and converted to text, and then matched to the list of supported commands. When a match is found, the corresponding command is executed using the `Voice Controller` module.

## Command Recognition Research
This part was used only for exploring the libraries. It is not used in the final project, but files are provided for reference.

## Recordings
Recordings for research were recorded by me in GarageBand and by default are kept in `recordings` folder, with a separate directory for each command. Those files are omitted from the repository.

## Authors
* **Paweł Saniewski** - *Everything except the Audio Player*
* **Mark Hillard** - *[Audio Player](https://codepen.io/markhillard/pen/jOOKxM)*

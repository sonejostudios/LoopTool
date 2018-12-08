# LoopTool
A collection of tools for audio loop files.


__Description:__

LoopTool is a collection of tools made for audio loops. LoopTool is able to split audio files into many equal parts or to extract a specific part, it can also put files in sequence or mix them together. It has also a lot more of handy features like applying fades, gain adjustement, normalize, convert to mono/stereo, etc etc... Its main goal is to prepare audio loops for live performence (with e.g. SuperBoucle, Luppp, Giada, Bitwig...). LoopTool is mainly based on SoX.

![screenshot](https://github.com/sonejostudios/LoopTool/blob/master/LoopTool105.png "LoopTool")


__Main Features:__

* Audio waveform
* Play via jack
* Graphical manipulations (divide, fades, select part)
* Load/Save file
* Set working directory
* Audiofile browser
* Queue list
* Grid and bpm
* Export click file
* Split files into equal parts
* Extract a specific part
* Apply fade in and fade out to the parts
* Change the gain
* Normalize
* Convert mono to stereo or stereo to mono
* Put audio files in sequence
* Mix audio files

  

__Installation:__

1. copy the whole LoopTool folder on your system
```
git clone https://github.com/sonejostudios/LoopTool.git
```

2. from this folder start LoopTool with: 
```
python3 LoopTool.py
```


__Requirements:__

* Python3
* Tkinter
* GNU/Linux (with SoX)
* PySoundfile
* sndfile-tools (https://github.com/erikd/sndfile-tools)


On Ubuntu/Mint:
```
sudo apt-get install python3 python3-tk sox sndfile-tools
```
Install PySoundFile via pip3:
```
pip3 install pysoundfile
```



__Notes:__

* LoopTool is for now a Linux-only Software. It was tested only on LinuxMint 17 MATE, but it should work also on Cinnamon, GNOME and KDE. No OSX and Windows versions are available.
* LoopTool was one of my playground for learning Python, so except a very bad code. For now it's fine for me, I learned a lot and it works, but it __definitely__ needs a complete rewrite.. If you have suggestions or you want to help, please contact me. Otherwise, have fun with it, I hope it will be helpful for you!


__Shortcuts:__

* Left-click on the waveform will select a part
* Right-click on the waveform will remove the selection
* Mouse-roll on any drop-down menu for a quick access (grid, fades, gain, divide)
* Enter manual values on almost all the entries (e.g. gain = 1.5)
* Space bar plays or stops the loaded file
* Double-click a file in the file browser will add that file to the queue list
* Double-click a file in the queue list will remove that file from the que list


__Entries and Buttons:__

Info:
* WAV-File: Copy/Paste a .wav file there or type its path
* ... : Opens a .wav file dialog
* Load: Loads the file into LoopTool
* Save As: Save the selected file as a new file (via save file dialog)
* Play: Plays the selected file via Jack (snd-jackplay)
* Stop: Stop playing
* Samples: Total length (in samples) of the selected file
* Seconds: Total length (in seconds) of the selected file
* Channels: Amount of audio chanels in the file (mono/stereo/etc)
* Samplerate: Samplerate of the selected file
* Grid: Grid for help
* Bpm: Calculates the bpm of the file according to the grid (4 beats/grid line)

One-File Editing:
* Fade In: Add fade in via presets. The last one is a grid length and will stick to it
* Fade out: Same as fade in, but for fade out
* Gain dB: Change file(s) gain(s) on export
* Normalize: Normalize file(s) gain(s) on export, this will overwrite Gain dB
* Mono/Stereo. Force Mono or Stereo. (Mix two stereo channels together to mono or split a mono channel to stereo)
* Split to files: Export all parts according to Divide
* Export/Extract Part: Export the selected part only
* Divide: Divides file into N parts
* Extract Part: The choosen part
* Part Length: Length of the selected part, in samples
* Start Point: Starting point of the selected part

File Browser:
* Shows the content of the working directory
* Delete File: Delete the file permanently
* ->: Add selected file to Queue List

Queue List (Many-Files Editing):
* Shows the files in the queue list for processing
* Remove: Remove selected file from the queue list
* Clear: Clear the queue
* Seq: Export all files in the queue list sequenced into one file (aka. Concatenate)
* Mix: Mix all files in the queue list together into one file

Working Directory:
* Workdir: Copy/paste file path or type the folder path.
* ...: Open path via dialog
* Load: Load path as a working directory for LoopTool





__Get started:__

* Open a working directory or a wave file, press load, done.


__Tips and Tricks:__

* Keep in mind, you can enter manual values on almost all the entries
* Split a loop into parts and sequence them in a new order
* Take the first or second half of a loop
* Apply gain changes or normalize
* Add fades
* Split mono to stereo or mix stereo into mono
* Try to figure out the bpm with the grid (4 beats in one grid part)





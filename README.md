# LoopTool
A collection of tools for audio loop files.


__Description:__

LoopTool is a collection of tools made for audio loops. LoopTool is able to split audio files into many equal parts or to extract a specific part, it can also put files in sequence or mix them together. It has also a lot more of handy features like appling fades, gain adjustement, normalize, convert to mono/stereo, etc etc... LoopTool is mainly based on SoX.

![screenshot](https://github.com/sonejostudios/LoopTool/blob/master/LoopTool104.png "LoopTool")


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
* klick (http://das.nasophon.de/klick/)


On Ubuntu/Mint:
```
sudo apt-get install python3 python3-tk sox sndfile-tools klick
```
Install PySoundFile via pip3:
```
pip3 install pysoundfile
```



__Notes:__

* LoopTool is for now a Linux-only Software. It was tested only on LinuxMint 17 MATE, but it should work also on Cinnamon, GNOME and KDE. No OSX and Windows versions are available.
* LoopTool was one of my playground for learning Python, so except a very bad code. For now it's fine for me, I learned a lot and it works, but it __definitely__ needs a complete rewrite.. If you have suggestions or you want to help, please contact me. Otherwise, have fun with it, I hope it will be helpful for you!



__Tips and Tricks:__

* Keep in mind, you can enter manual values on almost all the entries.
* Normalize you loops
* Export click trackvia klick
* Split a loop into parts and sequence them in a new order.
* 



__Buttons:__

* cd-drive : Split




__Configuration:__

* Open a working directory, press load, done.





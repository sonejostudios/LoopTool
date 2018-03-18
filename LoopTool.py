#!/usr/bin/env python3


from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from tkinter.filedialog import askopenfilename, askdirectory, asksaveasfilename

import os
import subprocess
from subprocess import Popen, PIPE
import time
from datetime import datetime

from threading import Thread

import glob

import soundfile as sf


version = "1.0.3"

white = "#ffffff"
black = "#000000"

fadepresets = ["0", "50", "100"]

gainpresets = ["-100"]
for i in range(13):
    gainpresets.append(i-6)

listboxlist = ["0", "50", "100"]

gridpresets = []
for i in range(1, 65):
    gridpresets.append(i)

queue = []

global playing_state
playing_state = False

play_looptime = 8




class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("LoopTool " + version)
        root.resizable(False, False)


        # waveframe infos
        self.waveframe = Frame(root)
        self.waveframe.bind("<KeyRelease-space>", self.play_file_toggle)
        self.waveframe.grid(row=0, column=0, padx=0, sticky=W)


        #Canvas
        self.wavcanvas = Canvas(self.waveframe, width=800, height=200)
        self.wavcanvas.bind("<Button-1>", self.click_on_canvas)
        self.wavcanvas.bind("<Button-3>", self.on_divide)
        self.wavcanvas.grid(row=0, column=0, padx=0, sticky=W)

        # Waveform
        self.picture = PhotoImage(file='waveform.png')
        self.picture2 = self.wavcanvas.create_image(400, 100, image=self.picture)


        # Entry WAV file
        self.wavfile_frame = Frame(self.waveframe)
        self.wavfile_label = Label(self.wavfile_frame, text="WAV-file :", justify=LEFT)
        self.wavfile_label.grid(row=0, column=0, sticky=W+E)

        self.wavfile_entry = Entry(self.wavfile_frame, width=58, background=white)
        self.wavfile_entry.bind("<Button-3>", self.entry_clear)
        self.wavfile_entry.grid(row=0, column=1)

        self.filechooser_button = ttk.Button(self.wavfile_frame, text="...", width=2, state="normal", command= self.open_file)
        self.filechooser_button.grid(row=0, column=2)

        self.fileload_button = ttk.Button(self.wavfile_frame, text="Load", width=4, state="normal", command= self.on_load_file)
        self.fileload_button.grid(row=0, column=3)

        self.fileload_button = ttk.Button(self.wavfile_frame, text="Save As", width=6, state="normal",command=self.save_as_file)
        self.fileload_button.grid(row=0, column=4)

        self.fileplay_button = ttk.Button(self.wavfile_frame, text="Play", width=9, state="normal", command=self.play_file)
        self.fileplay_button.grid(row=0, column=5)

        self.filestop_button = ttk.Button(self.wavfile_frame, text="Stop", width=6, state="disable",command=self.stop_playing)
        self.filestop_button.grid(row=0, column=6)

        self.wavfile_frame.grid(row=1, column=0, padx=0,  pady=0, sticky=W + E)


        # infos
        self.info_frame = Frame(self.waveframe)
        self.info_frame.grid(row=2, column=0, padx=0, sticky=W)


        self.samples_label = Label(self.info_frame, text="Samples :", justify=LEFT)
        self.samples_label.pack(side=LEFT)
        self.samples_entry = Entry(self.info_frame, width=15, background=white)
        self.samples_entry.pack(side=LEFT, pady=5)

        self.seconds_label = Label(self.info_frame, text="Seconds :", justify=LEFT)
        self.seconds_label.pack(side=LEFT)
        self.seconds_entry = Entry(self.info_frame, width=8, background=white)
        self.seconds_entry.pack(side=LEFT)

        self.channels_label = Label(self.info_frame, text="Channels :", justify=LEFT)
        self.channels_label.pack(side=LEFT)
        self.channels_entry = Entry(self.info_frame, width=2, background=white)
        self.channels_entry.pack(side=LEFT)

        self.samplerate_label = Label(self.info_frame, text="Samplerate :", justify=LEFT)
        self.samplerate_label.pack(side=LEFT)
        self.samplerate_entry = Entry(self.info_frame, width=8, background=white)
        self.samplerate_entry.pack(side=LEFT)


        self.grid_label = Label(self.info_frame, text="Grid :", justify=LEFT)
        self.grid_label.pack(side=LEFT)
        self.grid_entry = ttk.Combobox(self.info_frame, width=5, values=gridpresets)
        self.grid_entry.current(0)
        self.grid_entry.bind("<<ComboboxSelected>>", self.on_set_grid)
        self.grid_entry.bind("<Return>", self.on_set_grid)
        self.grid_entry.pack(side=LEFT)


        self.bpm_label = Label(self.info_frame, text="Bpm :", justify=LEFT)
        self.bpm_label.pack(side=LEFT)
        self.bpm_entry = Entry(self.info_frame, width=9, background=white)
        self.bpm_entry.pack(side=LEFT)



        # tool frame
        self.divide_frame = Frame(root, bd=1, relief=SUNKEN)
        self.divide_frame.grid(row=3, column=0, padx=0, pady=5, sticky=W+E)


        # on_fade_trigger
        self.fadein_label = Label(self.divide_frame, text="Fade In :", justify=LEFT)
        self.fadein_label.grid(row=0, column=0)
        self.fadein_entry = ttk.Combobox(self.divide_frame, width=6, values=fadepresets)
        self.fadein_entry.current(0)
        self.fadein_entry.bind("<Enter>", self.on_fade_trigger)
        self.fadein_entry.bind("<Return>", self.on_set_fadein_line)
        self.fadein_entry.bind("<<ComboboxSelected>>", self.on_set_fadein_line)
        self.fadein_entry.grid(row=0, column=1)

        self.fadeout_label = Label(self.divide_frame, text="Fade Out :", justify=LEFT)
        self.fadeout_label.grid(row=1, column=0)
        self.fadeout_entry = ttk.Combobox(self.divide_frame, width=6, values=fadepresets)
        self.fadeout_entry.current(0)
        self.fadeout_entry.bind("<Enter>", self.on_fade_trigger)
        self.fadeout_entry.bind("<Return>", self.on_set_fadeout_line)
        self.fadeout_entry.bind("<<ComboboxSelected>>", self.on_set_fadeout_line)
        self.fadeout_entry.grid(row=1, column=1)

        self.gain_label = Label(self.divide_frame, text="Gain dB:", justify=LEFT)
        self.gain_label.grid(row=0, column=2)
        self.gain_entry = ttk.Combobox(self.divide_frame, width=4, values=gainpresets)
        self.gain_entry.current(7)
        self.gain_entry.grid(row=0, column=3)


        self.norm_label = Label(self.divide_frame, text="Normalize :", justify=LEFT)
        self.norm_label.grid(row=0, column=4)
        self.norm = IntVar()
        self.norm_checkbox = Checkbutton(self.divide_frame, variable=self.norm)
        self.norm_checkbox.grid(row=0, column=5)

        self.mono_label = Label(self.divide_frame, text="Mono/Stereo :", justify=LEFT)
        self.mono_label.grid(row=1, column=4)
        self.mono = IntVar()
        self.mono_checkbox = Checkbutton(self.divide_frame, variable=self.mono)
        self.mono_checkbox.grid(row=1, column=5)



        # split/extract buttons
        self.splitbutton = ttk.Button(self.divide_frame, text="Split to Files", width=13, state="normal", command=self.on_split_file)
        self.splitbutton.grid(row=0, column=6, pady=5)

        self.trimbutton = ttk.Button(self.divide_frame, text="Extract Part", width=13, state="normal", command=self.on_trim_file)
        self.trimbutton.grid(row=1, column=6, pady=5)



        # divide
        self.divide_label = Label(self.divide_frame, text="Divide :", justify=LEFT)
        self.divide_label.grid(row=0, column=7)
        #self.divide_entry = Spinbox(self.divide_frame, from_=1, to_=999, justify=CENTER, width=5, command=self.divide)
        self.divide_entry = ttk.Combobox(self.divide_frame, width=5, values=gridpresets)
        self.divide_entry.current(0)
        self.divide_entry.bind("<<ComboboxSelected>>", self.on_divide)
        self.divide_entry.bind("<Return>", self.on_divide)
        self.divide_entry.grid(row=0, column=8)


        self.partlength_label = Label(self.divide_frame, text="Part Length :", justify=LEFT)
        self.partlength_label.grid(row=0, column=9)
        self.partlength_entry = Entry(self.divide_frame, width=10, background=white)
        self.partlength_entry.grid(row=0, column=10)

        self.takepart_label = Label(self.divide_frame, text="Extract Part :", justify=LEFT)
        self.takepart_label.grid(row=1, column=7)
        self.takepart_entry = Spinbox(self.divide_frame, from_=0, to_=2, justify=CENTER, width=5, command=self.select_part)
        self.takepart_entry.grid(row=1, column=8)

        self.startpoint_label = Label(self.divide_frame, text="Start Point :", justify=LEFT)
        self.startpoint_label.grid(row=1, column=9)
        self.startpoint_entry = Entry(self.divide_frame, width=10, background=white)
        self.startpoint_entry.grid(row=1, column=10)



        #listboxes
        self.listboxes_frame = Frame(root)
        self.listboxes_frame.grid(row=5, column=0, rowspan=1, columnspan=1, sticky=N+E+W, padx=5, pady=0)

        # Listbox
        self.listbox_frame = Frame(self.listboxes_frame)
        self.scrollbar = ttk.Scrollbar(self.listbox_frame, orient=VERTICAL)
        self.listbox = Listbox(self.listbox_frame, width=47, height=20, yscrollcommand=self.scrollbar.set, selectmode=BROWSE, activestyle=NONE)
        self.listbox.bind("<ButtonRelease-1>", self.on_get_file_path)
        self.listbox.bind("<Double-Button-1>", self.on_copy_to_queue)
        self.listbox.bind("<KeyRelease-space>", self.play_file_toggle)
        self.listbox.bind("<Return>", self.on_copy_to_queue)
        self.listbox.bind("<Delete>", self.on_delete_file)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=1)
        self.listbox_frame.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W, padx=0, pady=5)



        #  filebox buttons
        self.fileboxbutton_frame = Frame(self.listboxes_frame)
        self.fileboxbutton_frame.grid(row=2, column=0, rowspan=1, columnspan=1, sticky=N, padx=0, pady=5)

        # delete file
        self.deletefilebutton = ttk.Button(self.fileboxbutton_frame, text="Delete File", width=10, state="normal",
                                           command=self.delete_file)
        self.deletefilebutton.pack(side=LEFT)


        # copy to queue
        self.toqueuebutton = ttk.Button(self.fileboxbutton_frame, text="->", width=10, state="normal",
                                       command=self.copy_to_queue)
        self.toqueuebutton.pack(side=LEFT)



        #queue buttons
        self.queuebutton_frame = Frame(self.listboxes_frame)
        self.queuebutton_frame.grid(row=2, column=1, rowspan=1, columnspan=1, sticky=N, padx=0, pady=5)


        # remove from queue
        self.removelistbutton = ttk.Button(self.queuebutton_frame, text="Remove", width=7, state="normal",
                                           command=self.remove_from_queue)
        self.removelistbutton.pack(side=LEFT)


        # clear queue
        self.clearlistbutton = ttk.Button(self.queuebutton_frame, text="Clear", width=7, state="normal",
                                           command=self.clear_queue)
        self.clearlistbutton.pack(side=LEFT)

        # sequence queue
        self.removelistbutton = ttk.Button(self.queuebutton_frame, text="Seq", width=7, state="normal",
                                           command=self.on_seq)
        self.removelistbutton.pack(side=LEFT)

        # mix queue
        self.mixlistbutton = ttk.Button(self.queuebutton_frame, text="Mix", width=7, state="normal",
                                           command=self.on_mix)
        self.mixlistbutton.pack(side=LEFT)



        # Queuelist
        self.queuelistbox_frame = Frame(self.listboxes_frame)
        self.scrollbar = ttk.Scrollbar(self.queuelistbox_frame, orient=VERTICAL)
        self.queuelistbox = Listbox(self.queuelistbox_frame, width=47, height=20, yscrollcommand=self.scrollbar.set, selectmode=BROWSE, activestyle=NONE)
        #self.queuelistbox.bind("<Double-Button-1>", self.select_queue_item)
        self.queuelistbox.bind("<ButtonRelease-1>", self.select_queue_item)
        self.queuelistbox.bind("<Double-Button-1>", self.on_remove_from_queue)
        self.queuelistbox.bind("<KeyRelease-space>", self.play_file_toggle)
        self.queuelistbox.bind("<Delete>", self.on_remove_from_queue)
        self.scrollbar.config(command=self.queuelistbox.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.queuelistbox.pack(side=LEFT, fill=BOTH, expand=1)
        self.queuelistbox_frame.grid(row=1, column=1, rowspan=1, columnspan=1, sticky=W, padx=0, pady=5)



        # Folder
        self.folder_frame = Frame(root)
        self.folder_label = Label(self.folder_frame, text="Workdir :", justify=LEFT)
        self.folder_label.grid(row=0, column=0)

        self.folder_entry = Entry(self.folder_frame, width=82, background=white)
        self.folder_entry.bind("<Button-3>", self.entry_clear)
        self.folder_entry.grid(row=0, column=1, padx=5)

        self.folderchooser_button = ttk.Button(self.folder_frame, text="...", width=2, state="normal",
                                             command=self.open_folder)
        self.folderchooser_button.grid(row=0, column=2)

        # load folder button
        self.folderload_button = ttk.Button(self.folder_frame, text="Load", width=4, state="normal",
                                            command=self.thread_file_listbox)
        self.folderload_button.grid(row=0, column=3)


        self.folder_frame.grid(row=6, column=0, pady=5, sticky=W)



        # for testing only
        self.wavfile_entry.insert(0, "/media/sda7/Programming/Python/looptool/sin.wav")
        self.folder_entry.insert(0, "/media/sda7/Programming/Python/looptool/")

        self.load_file()

        self.thread_file_listbox()


        #set initial grid
        self.setgrid()





    def doNothing(self):
        print("do nothing")




    def click_on_canvas(self, event):
        print("clicked at", event.x, event.y)

        # only x needed
        x = event.x

        divider = int(self.divide_entry.get())
        partwidth = 800 / divider


        # get part no from canvas
        for i in range(divider):
            if x > partwidth*i and x < partwidth*i + partwidth:

                partno = i
                self.takepart_entry.delete(0,"end")
                self.takepart_entry.insert(1, partno+1)

                print("select part :", partno)

        self.select_part()

        # draw canvas selection
        self.wavcanvas.delete("selection")
        self.wavcanvas.create_rectangle((partwidth*partno), 000, (partwidth+partwidth*partno), 199, outline="white", fill="white", stipple='gray25', tag="selection")

        # update trim button
        self.trimbutton.config(state="normal")




    def on_delete_file(self, event):
        self.delete_file()

    def delete_file(self):
        print("delete file")

        delete_confirm = messagebox.askokcancel("Delete File", "Delete this File ?\n\n" + os.path.basename(self.wavfile_entry.get()))

        print(delete_confirm)

        if delete_confirm == True:
            command = "rm " + self.wavfile_entry.get()
            subprocess.Popen(command, shell=True)

            # update listbox
            self.file_listbox()
            # load new file
            self.get_file_path()

        else:
            pass



    def clear_queue(self):
        print("clear queue")

        global queue
        queue = []
        self.queuelistbox.delete(0, "end")



    def select_queue_item(self, event):
        print("select queue item")

        try:
            queuesel = queue[self.queuelistbox.curselection()[0]]
            queuesel2 = self.folder_entry.get() + queuesel

            self.wavfile_entry.delete(0, "end")
            self.wavfile_entry.insert(0, queuesel2)

            self.load_file()
        except:
            pass


    def on_remove_from_queue(self,event):
        self.remove_from_queue()

    def remove_from_queue(self):
        print("remove")

        self.queuecursel = self.queuelistbox.curselection()
        self.queuecursel2 = self.queuecursel[0]

        print(self.queuecursel2)

        global queue

        try:
            del queue[self.queuecursel2]
        except:
            pass

        self.queuelistbox.delete(0, "end")
        for i in queue:
            self.queuelistbox.insert("end", i)

        self.queuelistbox.select_set(self.queuecursel2)
        self.listbox.see(self.queuecursel2)


    def on_copy_to_queue(self, event):
        #self.nearest(event.y)
        self.copy_to_queue()


    def copy_to_queue(self):
        print("copy to queue")

        loop_basename = os.path.basename(self.wavfile_entry.get())
        #loop_basename = self.listbox.get(self.listbox.curselection())

        try:
            self.queuelistbox.select_set(self.queuecursel2+1)
        except:
            pass


        global queue
        queue.append(loop_basename)
        self.queuelistbox.delete(0, "end")

        ind = 0
        for i in queue:
            self.queuelistbox.insert("end", i)
            ind = ind + 1

        self.queuelistbox.select_set(ind)
        self.queuelistbox.see(ind)



    # sequence files
    def on_seq(self):

        mergeconf = messagebox.askokcancel("Sequence Files",
                                           "This will append all the files in the queue to :\n\nsequenced_loops.wav")

        if mergeconf == 1:
            self.seq()
        else:
            pass


    def seq(self):
        print("merge")
        queue_iter = 0
        command = "sox "

        for i in queue:
            path = self.folder_entry.get() + str(queue[queue_iter])

            command = command.__add__(path + " ")

            queue_iter = queue_iter + 1
            print(path)

        merge_path = self.folder_entry.get() + "sequenced_loops.wav"

        command = command.__add__(merge_path)
        finalcommand = command

        print(finalcommand)

        #merge files
        sox = subprocess.Popen(finalcommand, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = sox.communicate()

        # error handling
        try:
            subprocess.check_call(finalcommand, shell=True)

        except subprocess.CalledProcessError:
            stderr = stderr
            messagebox.showerror("Error", stderr)


        self.wavfile_entry.delete(0,"end")
        self.wavfile_entry.insert(0, merge_path)

        time.sleep(0.1)
        self.load_file()

        # update listbox
        self.thread_file_listbox()



    def on_mix(self):
        mergeconf = messagebox.askokcancel("Mix Files",
                                           "This will mix all the files in the queue to :\n\nmixed_loops.wav")

        if mergeconf == 1:
            self.mix()
        else:
            pass

    def mix(self):
        print("mix")
        queue_iter = 0
        command = "sox --combine mix "

        for i in queue:
            path = self.folder_entry.get() + str(queue[queue_iter])

            command = command.__add__(path + " ")

            queue_iter = queue_iter + 1
            print(path)

        merge_path = self.folder_entry.get() + "mixed_loops.wav"

        command = command.__add__(merge_path)
        finalcommand = command

        print(finalcommand)

        #mix files
        sox = subprocess.Popen(finalcommand, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = sox.communicate()

        # error handling
        try:
            subprocess.check_call(finalcommand, shell=True)

        except subprocess.CalledProcessError:
            stderr = stderr[14:]
            messagebox.showerror("Error", stderr)


        self.wavfile_entry.delete(0,"end")
        self.wavfile_entry.insert(0, merge_path)

        time.sleep(0.1)
        self.load_file()

        # update listbox
        self.thread_file_listbox()



    # divide
    def on_divide(self,event):
        self.divide()

        #reset
        # set takepart to 0, set trim button to export, delete start point, set full part length
        self.takepart_entry.delete(0, "end")
        self.takepart_entry.insert(0, 0)

        self.trimbutton.config(text="Export")

        if self.divider >1:
            self.trimbutton.config(state="disable")
        else:
            self.trimbutton.config(state="normal")

        self.startpoint_entry.delete(0,"end")
        self.startpoint_entry.insert(0, 0)



    def divide(self):

        self.divider = int(self.divide_entry.get())
        self.newlength = self.samples / self.divider

        self.partlength_entry.delete(0, "end")
        self.partlength_entry.insert(0, int(self.newlength))


        #remove selection
        self.wavcanvas.delete("selection")

        #draw lines
        global length800
        length800 = 800 / self.divider
        self.wavcanvas.delete("lines")
        for i in range(0, self.divider):
            self.wavcanvas.create_line(length800*i, 000, length800*i, 200, fill="white", tag="lines")

        # set take part
        self.takepart_entry.config(to_=self.divider)

        #force 1
        if int(self.divide_entry.get()) == 1 :
            self.takepart_entry.config(from_= 0, to_=1)

        self.takepart_entry.config(from_=0, to_=self.divider)

        #update
        self.select_part()

        #update fades
        self.set_fadein_line()
        self.set_fadeout_line()





    # grid
    def on_set_grid(self,event):
        self.setgrid()

    def setgrid(self):
        grid = int(self.grid_entry.get())


        # check if current == 12 (follow grid) and update
        if self.fadein_entry.current() == 12 and self.fadeout_entry.current() == 12:
            self.fade_trigger()
            self.fadein_entry.current(12)
            self.fadeout_entry.current(12)

        if self.fadein_entry.current() == 12:
            self.fade_trigger()
            self.fadein_entry.current(12)

        if self.fadeout_entry.current() == 12:
            self.fade_trigger()
            self.fadeout_entry.current(12)



        #draw lines
        global length800
        length800 = 800 / grid
        self.wavcanvas.delete("linesgrid")
        for i in range(0, grid):
            self.wavcanvas.create_line(length800*i, 000, length800*i, 200, fill="black", tag="linesgrid")


        # update
        self.select_part()

        #set grid part
        self.gridpart = int(self.samples / grid)

        # update fade presets
        self.fade_trigger()

        # redraw divide lines
        self.divide()

        #print(self.gridpart)
        #print(fadepresets)




    # take part startpoint
    def select_part(self):
        takepart = int(self.takepart_entry.get())

        # set start point
        startpoint = int(self.partlength_entry.get())  * (takepart-1)


        self.startpoint_entry.delete(0,"end")
        self.startpoint_entry.insert(0, str(startpoint))


        self.update_buttons()


        #reset startpoint
        if startpoint < 0:
            self.startpoint_entry.delete(0, "end")
            self.startpoint_entry.insert(0, 0)
            self.update_buttons()






    # trim export part
    def on_trim_file(self):
        filename = os.path.basename(self.wavfile_entry.get())
        parts = self.takepart_entry.get()

        splitconfirm = messagebox.askokcancel("Extract/Export",
                                           "This will extract/export the selected part to the following file :\n\n" + filename + ".part" + parts + ".wav")
        if splitconfirm == 1:
            self.trim_file()
        else:
            pass


    def trim_file(self):

        part = self.takepart_entry.get()

        if part == 0:
            self.takepart_entry.delete(0,"end")
            self.takepart_entry.insert(0, 1)
            self.startpoint_entry.insert(0, "0")
            part = 1


        wavefile = self.wavfile_entry.get()
        wavefileexport = wavefile + ".part"+ part +".wav"

        startpoint = self.startpoint_entry.get()
        partlenght = self.partlength_entry.get()

        self.fadein = self.fadein_entry.get()
        self.fadeout = self.fadeout_entry.get()

        gain = self.gain_entry.get()

        command = "sox " + wavefile + " " + wavefileexport + " trim " + startpoint + "s " + partlenght + "s "
        commandfadein = command + " fade " + self.fadein + "s "
        commandfadeinout = commandfadein + " fade 0 " + partlenght + "s " + self.fadeout + "s " + "gain " + gain

        print(commandfadeinout)

        self.norm_mono()

        finalcommand = commandfadeinout + self.commandmono + self.commandnorm

        #process command
        print(finalcommand)
        sox = subprocess.Popen(finalcommand, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = sox.communicate()
        stderr = stderr[:]
        if "sox" in str(stderr):
            messagebox.showerror("Error", stderr)

        # update listbox
        self.thread_file_listbox()



    # split apart
    def on_split_file(self):
        filename = os.path.basename(self.wavfile_entry.get())
        parts = self.divide_entry.get()
        filelist = ""
        for i in range(int(parts)):
            fullfilename = str(filename) + ".split" + str(i+1)+ ".wav\n"
            filelist += fullfilename
        splitconfirm = messagebox.askokcancel("Split Files",
                                           "This will split the file to the following " + parts +" files :\n\n" + filelist)
        if splitconfirm == 1:
            self.split_file()
        else:
            pass


    def split_file(self):

        wavefile = self.wavfile_entry.get()
        partlenght = self.partlength_entry.get()

        self.fadein = self.fadein_entry.get()
        self.fadeout = self.fadeout_entry.get()

        self.norm_mono()

        gain = self.gain_entry.get()

        for i in range(0, self.divider):
            wavefileexport = wavefile + ".split" +str(i+1) +".wav"

            startpoint2 = str(int(partlenght)*i)

            command = "sox " + wavefile + " " + wavefileexport + " trim " + startpoint2 + "s " + partlenght + "s"
            commandfadein = command + " fade " + self.fadein + "s"
            commandfadeinout = commandfadein + " fade 0 " + partlenght + "s " + self.fadeout + "s " + "gain " + gain

            finalcommand = commandfadeinout + self.commandmono + self.commandnorm

            print(finalcommand)
            sox = subprocess.Popen(finalcommand, shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = sox.communicate()


        if "sox" in str(stderr):
            messagebox.showerror("Error", stderr)


        # update listbox
        self.thread_file_listbox()



    # create commands for normalizing and mix to mono
    def norm_mono(self):
        normstate = self.norm.get()
        monostate = self.mono.get()

        if normstate == 1:
            self.commandnorm = " norm -1 "
        else:
            self.commandnorm = " "

        if monostate == 0:
            self.commandmono = " channels 1 "
        else:
            self.commandmono = " channels 2 "


    def on_fade_trigger(self, event):
        self.fade_trigger()


    def fade_trigger(self):

        # set fade presets
        sampleratequarter = self.samplerate / 4
        sampleratehalf = self.samplerate / 2
        sampleratetwice = self.samplerate * 2
        partlength = self.partlength_entry.get()
        self.gridpart = self.samples / int(self.grid_entry.get())

        global fadepresets
        fadepresets = [0, 50, 100, 1000, 2000, 3000, 4000, 6000, int(sampleratequarter), int(sampleratehalf), int(self.samplerate), int(sampleratetwice), int(self.gridpart)]
        self.fadein_entry["values"] = fadepresets
        self.fadeout_entry["values"] = fadepresets


    # load file
    def on_load_file(self):
        self.load_file()

        self.folder_entry.delete(0,"end")
        self.folder_entry.insert(0, self.wavfile_entry.get())

        self.thread_file_listbox()


    def load_file(self):

        # get infos
        f = sf.SoundFile(self.wavfile_entry.get())
        global samples, seconds, channels, samplerate
        self.samples = len(f)
        self.seconds = len(f) / f.samplerate
        self.channels = f.channels
        self.samplerate = f.samplerate


        self.samples_entry.delete(0,"end")
        self.samples_entry.insert(0, self.samples)

        self.seconds_entry.delete(0, "end")
        self.seconds_entry.insert(0, "%.3f" % self.seconds)

        self.channels_entry.delete(0, "end")
        self.channels_entry.insert(0, self.channels)

        self.samplerate_entry.delete(0, "end")
        self.samplerate_entry.insert(0, self.samplerate)


        # starting values
        self.partlength_entry.delete(0, "end")
        self.partlength_entry.insert(0, self.samples)

        self.startpoint_entry.delete(0, "end")
        self.startpoint_entry.insert(0, "0")

        self.divide()
        self.select_part()

        #trigger fade presets
        self.fade_trigger()

        self.update_buttons()

        #set mono stereo checkbox
        if self.channels == 1:
            self.mono_checkbox.deselect()
        else:
            self.mono_checkbox.select()


        # draw and import waveform
        command = "sndfile-waveform -c -1 -S 0 " + self.wavfile_entry.get() + " waveform.png"

        os.system(command)

        # update waveform
        global picture3
        picture3 = PhotoImage(file='waveform.png')
        self.wavcanvas.itemconfigure(self.picture2, image=picture3)


        #update buttons
        self.update_buttons()


    # listbox update thread
    def thread_file_listbox(self):
        t2 = Thread(target=self.file_listbox)
        t2.start()



    #listbox update
    def file_listbox(self):

        self.list_item_index = self.listbox.index(ACTIVE)

        # wait until file manipulation is done
        time.sleep(0.1)

        self.folder_path =  os.path.dirname(self.folder_entry.get())
        self.folder_entry.delete(0, "end")
        self.folder_entry.insert(0, self.folder_path + "/")

        # get all wav files in the workdir
        filelist = glob.glob(self.folder_path + "/*.wav") + glob.glob(self.folder_path + "/*.lt")
        filelist.sort()

        listboxlist = filelist

        self.listbox.delete(0, "end")
        for i in listboxlist:
            basename = os.path.basename(i)
            self.listbox.insert("end", basename)


        #re-set selection after updateing
        self.listbox.activate(self.list_item_index)
        self.listbox.selection_set(self.list_item_index)

        self.listbox.see(self.list_item_index)



    def on_get_file_path(self, event):
        self.get_file_path()


    def get_file_path(self):
        self.list_item = self.folder_path + "/" + self.listbox.get(self.listbox.curselection())
        print(self.list_item)
        self.select_in_list()



    def select_in_list(self):

        self.wavfile_entry.delete(0,"end")
        #self.list_item = self.listbox.get(self.listbox.curselection())

        print(self.list_item)
        self.wavfile_entry.insert(0, self.list_item)


        self.load_file()

        self.stop_playing()

        #update selection

        # draw cavas selection
        diventry = int(self.divide_entry.get())
        partentry = int(self.takepart_entry.get())-1
        partwidth = 800 / diventry
        self.wavcanvas.delete("selection")

        self.wavcanvas.create_rectangle((partwidth*partentry), 000, partwidth + partwidth*partentry, 199, outline="white",
                                        fill="white", stipple='gray25', tag="selection")


        self.trimbutton.config(text="Export")


    # play
    def play_file_toggle(self, event):

        print("playing " + str(playing_state))

        if playing_state == True:
            self.list_item = self.wavfile_entry.get()
            self.stop_playing()

        else:
            self.list_item = self.wavfile_entry.get()
            self.play_file()



    def play_file(self):
        global playing_state
        playing_state = True

        file = self.wavfile_entry.get()

        command = "sndfile-jackplay " + file + " -l " + str(play_looptime)
        subprocess.Popen(command, shell=True)


        # start playhead thread
        self.t1 = Thread(target=self.playhead_thread, name ="JackPlay")
        self.t1.start()

        self.fileplay_button.config(state="disable")
        self.filestop_button.config(state="normal")


    def stop_playing(self):
        global playing_state
        playing_state = False

        command = "killall sndfile-jackplay"
        subprocess.Popen(command, shell=True)


        self.fileplay_button.config(state="normal")
        self.filestop_button.config(state="disable")



    # playhead
    def playhead_thread(self):
        start_time = datetime.now()
        elapsed_seconds = 0.0

        while float(elapsed_seconds) < self.seconds * play_looptime and playing_state == True:
            time_elapsed = datetime.now() - start_time
            time2 = str(time_elapsed)
            elapsed_seconds = time2[5:11]

            time3 = float(elapsed_seconds) * (800/self.seconds)
            time4 = time3  % 800


            self.wavcanvas.delete("playhead")
            self.wavcanvas.create_line(time4, 200, time4, 000, fill="white", tag="playhead")

            time.sleep(0.01)

        # delete playhead when finished
        self.wavcanvas.delete("playhead")

        # update play and stop button states
        self.fileplay_button.config(state="enable")
        self.filestop_button.config(state="disable")





    def update_buttons(self):

        self.splitbutton.config(text="Split to Files (" + self.divide_entry.get() + ")")
        self.trimbutton.config(text="Extract Part " + self.takepart_entry.get() )


        if self.divider == 1:
            self.splitbutton.config(state="disable")
            self.trimbutton.config(text="Export")
        else:
            self.splitbutton.config(state="normal")


        self.count_bpm()




    def count_bpm(self):

        length = self.seconds
        divider = self.grid_entry.get()

        bpm = int(divider) * 4 / float(length)
        bpm2 = bpm * 60

        self.bpm_entry.delete(0, "end")
        self.bpm_entry.insert(0, bpm2)



    # clear entry with mouse button3
    def entry_clear(self, event):
        try:
            event.widget.delete(0, "end")
            event.widget.focus_set()
        except:
            event.widget.delete(0.0, "end")
            event.widget.focus_set()


    # file chooser wav
    def open_file(self):
        FILEOPENOPTIONS = dict(defaultextension='.wav',
                               filetypes=[('WAV-files', '*.wav'), ('All files', '*.*')], initialdir=self.folder_entry.get())
        self.list_item = askopenfilename(**FILEOPENOPTIONS)
        if self.list_item != "":
            self.wavfile_entry.delete(0, "end")
            self.wavfile_entry.insert(0, self.list_item)

            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, os.path.dirname(self.list_item) + "/")

            self.select_in_list()
        else:
            pass



    # file chooser folder
    def open_folder(self):
        DIROPENOPTIONS = dict(initialdir=self.folder_entry.get())
        self.folderpath = askdirectory(**DIROPENOPTIONS)
        if self.folderpath != "":
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, self.folderpath  + "/")
            self.file_listbox()

            self.wavfile_entry.delete(0, "end")
            self.wavfile_entry.insert(0, self.folderpath  + "/" + self.listbox.get(0))

            self.load_file()

        else:
            pass



    # file chooser save as file
    def save_as_file(self):
        FILEOPENOPTIONS = dict(defaultextension='.wav',
                               filetypes=[('WAV-files', '*.wav'), ('All files', '*.*')], initialdir=self.folder_entry.get())

        result = asksaveasfilename(**FILEOPENOPTIONS)

        command = "cp " + self.folder_entry.get() + os.path.basename(self.wavfile_entry.get()) + " " + result

        print(command)

        try:
            os.system(command)
        except:
            pass

        # update listbox
        self.file_listbox()



    #fade in lines
    def on_set_fadein_line(self, event):
        self.set_fadein_line()

    def set_fadein_line(self):
        fadevalue = int(self.fadein_entry.get())
        fadepos = (fadevalue / self.samples) * 800

        divider = int(self.divide_entry.get())
        partwidth = 800 / divider

        self.wavcanvas.delete("fadein")

        if fadevalue != 0:
            for i in range(divider):
                #self.wavcanvas.create_line(fadepos+partwidth*i, 000, partwidth*i, 200, fill="gray", tag="fadein", smooth=True, width=2)
                self.wavcanvas.create_polygon(1+fadepos + partwidth * i, 000, 1+partwidth * i, 200, 1+partwidth * i, 000, fill="gray", tag="fadein", width=1)



    #fade out lines
    def on_set_fadeout_line(self, event):
        self.set_fadeout_line()

    def set_fadeout_line(self):
        fadevalue = int(self.fadeout_entry.get())
        fadepos = (fadevalue / self.samples) * 800

        divider = int(self.divide_entry.get())
        partwidth = 800 / divider

        self.wavcanvas.delete("fadeout")

        if fadevalue != 0:
            for i in range(divider):
                #self.wavcanvas.create_line(800-(fadepos+partwidth*i), 000, 800-(partwidth*i), 200, fill="gray", tag="fadeout", smooth=True, width=2)
                self.wavcanvas.create_polygon(800 - (fadepos + partwidth * i), 000, 800 - (partwidth * i), 200, 800 - (partwidth * i), 000, fill="gray", tag="fadeout", width=1)




# Main Calls
##############################
root = Tk()
my_gui = MainWindow(root)

#root.protocol('WM_DELETE_WINDOW', stop_playing)
root.mainloop()

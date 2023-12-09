#test
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.filedialog import askopenfile

class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        #label
        self.label = ttk.Label(win, text="Pick a File: ")
        self.label.pack(pady = 10)

        #file button
        self.browse = ttk.Button(win, text="Browse Files", command=browseFile).pack(pady=15)

    
    def browseFile(self):
        file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file:
            self.audio = file
            self.audio.exportasWav(file)

    #sets the controller
    def set_controller(self, controller):
        self.controller = controller

    #graph and data display
    def graphDataDisplay(self, model):
        self.model = model
        time = self.model.audioLength(file)
        self.lengthAudio = ttk.Label(self, text=f"The length of the audio is {time}")
        #show waveform in a Frame
        #display frequencies
        #display RT60 plots (show difference down to 0.5 sec)
        #Button to combine plots
        #OPTIONAL: add Buttons to alternate between frequencies

    


import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.filedialog import askopenfile
from matplotlib.figure import Figure
from matplotlib import gridspec
from model import ProcessAudio
from model import ComputeAudio

class View(ttk.Frame):
    def __init__(self):
        super().__init__()
        #self.minsize(width=650, height=500)
        #self.maxsize(width=650, height=500)     
        #label
        self.label = ttk.Label(self, text="Load a File: ")
        self.label.pack(pady = 10)
        

    def browseFile(self):
        file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file:
            self.audio = file
            self.audio.exportasWav(file)

    #sets the controller
    def set_controller(self, controller):
        self.controller = controller
        #file button
        self.browse = ttk.Button(self, text="Browse Files", command=self.controller.browseFile).pack(pady=15)

    #graph and data display
    def graphDataDisplay(self, model):
        self.model = model
        time = self.model.audioLength(file)
        self.lengthAudio = ttk.Label(self, text=f"The length of the audio is {time}")

        #show waveform in a Frame
        wave = ttk.Frame(self).pack(pady=10)
        waveGraph = Figure()
        canvas = FigureCanvasTkAgg(waveGraph, wave)
        wave.pack(fill=tk.BOTH, expand=1)
        self.controller.displayWave()


        #display frequencies
        lowfreq = ttk.Frame(self).pack(pady=10)
        lowPlotFreq = Figure()
        self.controller.lowFreqPlot()

        midfreq = ttk.Frame(self).pack(pady=10)
        midPlotFreq = Figure()
        self.controller.midFreqPlot()

        highfreq = ttk.Frame(self).pack(pady=10)
        highPlotFreq = Figure()
        self.controller.highFreqPlot()
        
        #display RT60 plots (show difference down to 0.5 sec)
        self.displayAve = ttk.Label(self, text=f"{self.controller.calcAverage}")

        #Button to combine plots
        self.combine = ttk.Button(self, text="Combine Plots", command=self.controller.displayFreqs).pack(pady=15)
        #OPTIONAL: add Buttons to alternate between frequencies

if __name__ == '__main__':
    app = View()
    app.mainloop()
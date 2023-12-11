import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib import gridspec
from controller import Controller
import matplotlib.pyplot as plt

class View(tk.Tk):
    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.onClose)
        self.geometry('500x500')
        self.title("Audio Analyzer and Visualizer")
        self.filePath = tk.StringVar() # stores file path str
        
        btn = tk.Button(self, text="Browse Audio File", command=self.browseFile, height=3, width=20)
        btn.pack(side=tk.TOP, pady=20)

        specgram_btn = tk.Button(self, text="Specgram", command=lambda: self.displayGraph("extra"), height=3, width=15)
        specgram_btn.pack(side=tk.TOP)

        self.status_textVar = tk.StringVar()
        self.status_textVar.set("No File Selected")
        status = tk.Label(self, textvariable=self.status_textVar)
        status.pack(side=tk.TOP)

        self.resonantFreq = tk.StringVar()

        self.length_textVar = tk.StringVar()
        length_display = tk.Label(self, textvariable=self.length_textVar)
        length_display.pack(side=tk.TOP)

        self.RT60_textVar = tk.StringVar()
        self.RT60_textVar.set("Select Frequency to display RT60. Select Combined to see average rt60")
        rt60_label = tk.Label(self, textvariable=self.RT60_textVar)
        rt60_label.pack()

        combined_btn = tk.Button(self, text="Combined", command=lambda: self.displayGraph("combined"), width=10)
        combined_btn.pack(side=tk.BOTTOM, pady=15)
        raw_btn = tk.Button(self, text="Raw", command=lambda: self.displayGraph("raw"), width=10)
        raw_btn.pack(side=tk.BOTTOM, padx=50)

        low_btn = tk.Button(self, text="Low", command=lambda: self.displayGraph("low"), height=3, width=10)
        low_btn.pack(side=tk.TOP)
        mid_btn = tk.Button(self, text="Mid", command=lambda: self.displayGraph("mid"), height=3, width=10)
        mid_btn.pack(side=tk.TOP)
        high_btn = tk.Button(self, text="High", command=lambda: self.displayGraph("high"), height=3, width=10)
        high_btn.pack(side=tk.TOP)
        


        



    
    
    def onClose(self):
        plt.clf()
        plt.close()
        self.destroy()

    def browseFile(self):
        file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.m4a")]) # get file path 
        self.filePath.set(file) # save file path to stringvar
        # print(self.filePath.get())
        self.con = Controller(file)
        self.status_textVar.set(f'File selected: {file}')
        self.length_textVar.set(f'Audio Length {round(self.con.audio_length, 2)}')
        self.resonantFreq.set(f'Resonant Frequency: {self.con.getResonantFreq()}')

    def displayGraph(self, frequency: str):
        if(not self.filePath.get()):
            print("No valid path")
            return
        if (frequency=="low"):
            rt60 = self.con.lowFreqPlot()
            self.RT60_textVar.set(f'The RT60 for low frequency is {round(rt60, 2)} seconds')
        elif (frequency=="mid"):
            rt60 = self.con.midFreqPlot()
            self.RT60_textVar.set(f'The RT60 for mid frequency is {round(rt60, 2)} seconds')
        elif (frequency=="high"):
            rt60 = self.con.highFreqPlot()
            self.RT60_textVar.set(f'The RT60 for high frequency is {round(rt60, 2)} seconds')
        elif (frequency=="combined"):
            self.con.displayCombinedFreqs()
            self.RT60_textVar.set(f'The average RT60 is {round(self.con.calcRT60_difference()[0], 2)} seconds. The difference from 0.5s is {round(self.con.calcRT60_difference()[1], 2)} seconds')
        elif (frequency=="raw"):
            self.con.displayWave()
            self.RT60_textVar.set("")
        elif (frequency== "extra"):
            self.con.displaySpecgram()
            self.RT60_textVar.set("")

        else:
            return


if __name__ == '__main__':
    app = View()
    app.mainloop()
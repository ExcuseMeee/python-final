from model import ProcessAudio
from model import ComputeAudio

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
    
    def browseFile(self):
        file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file:
            self.model.audio = file
            self.model.audio.exportasWav(file)

    def lowFreqPlot(self):
        # low frequency
        # calculate RT60
        lowFreqRT20 = (
            lowFreq_maxVal_m25_orderedPair[0] - lowFreq_maxVal_orderedPair[0]
        )  # final time - initial time
        lowFreqRT60 = 3 * lowFreqRT20
        print(f"The RT60 for low frequency ({freqs[lowFreqIndex]}Hz) is {lowFreqRT60} sec")
        plt.plot(times, lowFreqSpecData)
        plt.scatter(
            lowFreq_maxVal_orderedPair[0], lowFreq_maxVal_orderedPair[1], c="red"
        )  # mark max value
        plt.scatter(
            lowFreq_maxVal_m25_orderedPair[0], lowFreq_maxVal_m25_orderedPair[1], c="blue"
        )  # mark max value - 25
        plt.title(f"Plot of Intensity vs Time for {freqs[lowFreqIndex]}Hz frequency")
        plt.xlabel("Time (s)")
        plt.ylabel("Intensity (dB)")
        plt.show()
    
    def midFreqPlot(self):
        # mid frequency
        # calculate RT60
        midFreqRT20 = midFreq_maxVal_m25_orderedPair[0] - midFreq_maxVal_orderedPair[0] # final time - initial time
        midFreqRT60 = 3 * midFreqRT20
        print(f'The RT60 for mid frequency ({freqs[midFreqIndex]}Hz) is {midFreqRT60} sec')
        plt.plot(times, midFreqSpecData)
        plt.scatter(midFreq_maxVal_orderedPair[0], midFreq_maxVal_orderedPair[1], c="red") # mark max value
        plt.scatter(midFreq_maxVal_m25_orderedPair[0], midFreq_maxVal_m25_orderedPair[1], c="blue") # mark max value - 25
        plt.title(f'Plot of Intensity vs Time for {freqs[midFreqIndex]}Hz frequency')
        plt.xlabel("Time (s)")
        plt.ylabel("Intensity (dB)")
        plt.show()

    def highFreqPlot(self):
        # high frequency
        # calculate RT60
        highFreqRT20 = highFreq_maxVal_m25_orderedPair[0] - highFreq_maxVal_orderedPair[0] # final time - initial time
        highFreqRT60 = 3 * highFreqRT20
        print(f'The RT60 for high frequency ({freqs[highFreqIndex]}Hz) is {highFreqRT60} sec')
        plt.plot(times, highFreqSpecData)
        plt.scatter(highFreq_maxVal_orderedPair[0], highFreq_maxVal_orderedPair[1], c="red") # mark max value
        plt.scatter(highFreq_maxVal_m25_orderedPair[0], highFreq_maxVal_m25_orderedPair[1], c="blue") # mark max value - 25
        plt.title(f'Plot of Intensity vs Time for {freqs[highFreqIndex]}Hz frequency')
        plt.xlabel("Time (s)")
        plt.ylabel("Intensity (dB)")
        plt.show()

    def displayWave(self):
        raw_data = c.scipy_wav_data
        length = c.audioLength
        t_axis = np.linspace(0, length, raw_data.shape[0])
        plt.plot(t_axis, raw_data)
        plt.title("Raw Waveform")
        plt.show()
    
    def displayFreqs(self):
        plt.plot(times, lowFreqSpecData, label="low")
        plt.plot(times, midFreqSpecData, label="mid")
        plt.plot(times, highFreqSpecData, label="high")
        plt.legend() # required to differentiate between graphs
        plt.title("Combined")
        plt.show()
        
    def calcAverage(self):
        avg_rt60 = (self.model.lowFreqRT60 + self.model.midFreqRT60 + self.model.highFreqRT60) / 3

        difference = avg_rt60 - 0.5

        print(f"Avg rt60 = {avg_rt60}. Difference from 0.5sec = {difference}")


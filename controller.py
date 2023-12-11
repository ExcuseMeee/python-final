from model import ProcessAudio
from model import ComputeAudio
import numpy as np
import matplotlib.pyplot as plt


class Controller:
    def __init__(self, raw_audioFile_path: str) -> None:
        audio = ProcessAudio(raw_audioFile_path)
        audio.exportAsWav()

        self.model = ComputeAudio(audio.destinationPath)
        self.computedSpectrumData = self.model.computeSpectrumData()
        self.specgramDataTuple = self.model.specgramDataTuple
        self.rt20Data = self.model.computeRT20()
        self.resonanceFreq = self.model.computeResonantFreq()

        self.raw_data = self.model.scipy_wav_data
        self.audio_length = self.model.audioLength

    def lowFreqPlot(self):
        (
            (lowFreqIndex, lowFreqSpecData),
            (midFreqIndex, midFreqSpecData),
            (highFreqIndex, highFreqSpecData),
        ) = self.computedSpectrumData

        spectrum, freqs, times, im = self.specgramDataTuple

        (
            (lowFreqIndex, lowFreq_maxVal_orderedPair, lowFreq_maxVal_m25_orderedPair),
            (midFreqIndex, midFreq_maxVal_orderedPair, midFreq_maxVal_m25_orderedPair),
            (
                highFreqIndex,
                highFreq_maxVal_orderedPair,
                highFreq_maxVal_m25_orderedPair,
            ),
        ) = self.rt20Data

        # plot graphs. graphs will show the line and also two points which indicate the RT20 vals
        # low frequency
        # calculate RT60
        lowFreqRT20 = (
            lowFreq_maxVal_m25_orderedPair[0] - lowFreq_maxVal_orderedPair[0]
        )  # final time - initial time
        lowFreqRT60 = 3 * lowFreqRT20
        plt.plot(times, lowFreqSpecData)
        plt.scatter(
            lowFreq_maxVal_orderedPair[0], lowFreq_maxVal_orderedPair[1], c="red"
        )  # mark max value
        plt.scatter(
            lowFreq_maxVal_m25_orderedPair[0],
            lowFreq_maxVal_m25_orderedPair[1],
            c="blue",
        )  # mark max value - 25
        plt.title(f"Plot of Intensity vs Time for {freqs[lowFreqIndex]}Hz frequency")
        plt.xlabel("Time (s)")
        plt.ylabel("Intensity (dB)")
        plt.show()
        return lowFreqRT60

    def midFreqPlot(self):
        (
            (lowFreqIndex, lowFreqSpecData),
            (midFreqIndex, midFreqSpecData),
            (highFreqIndex, highFreqSpecData),
        ) = self.computedSpectrumData

        spectrum, freqs, times, im = self.specgramDataTuple

        (
            (lowFreqIndex, lowFreq_maxVal_orderedPair, lowFreq_maxVal_m25_orderedPair),
            (midFreqIndex, midFreq_maxVal_orderedPair, midFreq_maxVal_m25_orderedPair),
            (
                highFreqIndex,
                highFreq_maxVal_orderedPair,
                highFreq_maxVal_m25_orderedPair,
            ),
        ) = self.rt20Data

        # plot graphs. graphs will show the line and also two points which indicate the RT20 vals
        # mid frequency
        # calculate RT60
        midFreqRT20 = (
            midFreq_maxVal_m25_orderedPair[0] - midFreq_maxVal_orderedPair[0]
        )  # final time - initial time
        midFreqRT60 = 3 * midFreqRT20
        plt.plot(times, midFreqSpecData)
        plt.scatter(
            midFreq_maxVal_orderedPair[0], midFreq_maxVal_orderedPair[1], c="red"
        )  # mark max value
        plt.scatter(
            midFreq_maxVal_m25_orderedPair[0],
            midFreq_maxVal_m25_orderedPair[1],
            c="blue",
        )  # mark max value - 25
        plt.title(f"Plot of Intensity vs Time for {freqs[midFreqIndex]}Hz frequency")
        plt.xlabel("Time (s)")
        plt.ylabel("Intensity (dB)")
        plt.show()
        return midFreqRT60

    def highFreqPlot(self) -> float:
        (
            (lowFreqIndex, lowFreqSpecData),
            (midFreqIndex, midFreqSpecData),
            (highFreqIndex, highFreqSpecData),
        ) = self.computedSpectrumData

        spectrum, freqs, times, im = self.specgramDataTuple

        (
            (lowFreqIndex, lowFreq_maxVal_orderedPair, lowFreq_maxVal_m25_orderedPair),
            (midFreqIndex, midFreq_maxVal_orderedPair, midFreq_maxVal_m25_orderedPair),
            (
                highFreqIndex,
                highFreq_maxVal_orderedPair,
                highFreq_maxVal_m25_orderedPair,
            ),
        ) = self.rt20Data

        # plot graphs. graphs will show the line and also two points which indicate the RT20 vals
        # high frequency
        # calculate RT60
        highFreqRT20 = (
            highFreq_maxVal_m25_orderedPair[0] - highFreq_maxVal_orderedPair[0]
        )  # final time - initial time
        highFreqRT60 = 3 * highFreqRT20
        plt.plot(times, highFreqSpecData)
        plt.scatter(
            highFreq_maxVal_orderedPair[0], highFreq_maxVal_orderedPair[1], c="red"
        )  # mark max value
        plt.scatter(
            highFreq_maxVal_m25_orderedPair[0],
            highFreq_maxVal_m25_orderedPair[1],
            c="blue",
        )  # mark max value - 25
        plt.title(f"Plot of Intensity vs Time for {freqs[highFreqIndex]}Hz frequency")
        plt.xlabel("Time (s)")
        plt.ylabel("Intensity (dB)")
        plt.show()
        return highFreqRT60

    def displayWave(self) -> None:
        raw_data = self.raw_data
        length = self.audio_length
        t_axis = np.linspace(0, length, raw_data.shape[0])

        # plot graphs

    def displayCombinedFreqs(self) -> None:
        (
            (lowFreqIndex, lowFreqSpecData),
            (midFreqIndex, midFreqSpecData),
            (highFreqIndex, highFreqSpecData),
        ) = self.computedSpectrumData

        spectrum, freqs, times, im = self.specgramDataTuple

        plt.plot(times, lowFreqSpecData, label="low")
        plt.plot(times, midFreqSpecData, label="mid")
        plt.plot(times, highFreqSpecData, label="high")
        plt.legend()  # required to differentiate between graphs
        plt.title("Combined")
        plt.show()

    def calcRT60_difference(self):
        (
            (lowFreqIndex, lowFreq_maxVal_orderedPair, lowFreq_maxVal_m25_orderedPair),
            (midFreqIndex, midFreq_maxVal_orderedPair, midFreq_maxVal_m25_orderedPair),
            (
                highFreqIndex,
                highFreq_maxVal_orderedPair,
                highFreq_maxVal_m25_orderedPair,
            ),
        ) = self.rt20Data
        # spectrum, freqs, times, im = self.specgramDataTuple
        lowRT60 = 3 * (
            lowFreq_maxVal_m25_orderedPair[0] - lowFreq_maxVal_orderedPair[0]
        )
        midRT60 = 3 * (
            midFreq_maxVal_m25_orderedPair[0] - midFreq_maxVal_orderedPair[0]
        )
        highRT60 = 3 * (
            highFreq_maxVal_m25_orderedPair[0] - highFreq_maxVal_orderedPair[0]
        )

        avgRT60 = (lowRT60 + midRT60 + highRT60) / 3
        difference = avgRT60 - 0.5

        return (avgRT60, difference)

'''
# NOTE: EXAMPLE CODE, uncomment for testing. delete in prod
# using the controller
con = Controller("media/Clap.m4a")
avgRT60, difference = con.calcRT60_difference() # this function returns the average rt60 and the difference
lowFreqRT60 = con.lowFreqPlot() # this function plots the low freq AND returns the RT60 value
midFreqRT60 = con.midFreqPlot() # this function plots the mid freq AND returns the RT60 value
highFreqRT60 = con.highFreqPlot() # this function plots the high freq AND returns the RT60 value

# diplay avgrt60, difference, lowFreqRT60, midFreqRT60, highFreqRT60 using tkinter in view.py
'''

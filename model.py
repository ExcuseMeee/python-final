from pathlib import Path
from pydub import AudioSegment
import os
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np


class ProcessAudio:
    def __init__(self, filePath: str) -> None:
        self.validFileTypes = [".wav", ".m4a", ".mp3"]
        self.filePath = filePath
        self.fileType = Path(filePath).suffix

        self.isValid = self.fileType in self.validFileTypes
        self.destinationPath = ""

    def cleanAudio(self) -> AudioSegment:
        """
        Helper Method, do not call directly
        """
        if not self.isValid:
            return

        format = (self.fileType)[1:]

        rawAudio: AudioSegment = AudioSegment.from_file(self.filePath, format=format)
        monoAudio = rawAudio.set_channels(1)

        return monoAudio

    def exportAsWav(self):
        """
        Export the current ProcessAudio object as wav file to media/ folder\n
        Will not export if fileType of object is not valid
        """
        monoAudio = self.cleanAudio()

        if not monoAudio:
            return

        if not os.path.exists("media"):
            os.mkdir("media")

        dest = "media/cleanedAudio.wav"

        self.destinationPath = dest

        monoAudio.export(dest, format="wav")


class ComputeAudio:
    def __init__(self, pathToWav: str) -> None:
        rate, data = wavfile.read(pathToWav)

        self.rate = rate
        self.scipy_wav_data = data
        self.audioLength = data.shape[0] / rate
        self.specgramDataTuple = ()

    def computeSpecgram(self):
        """
        Helper method, do not call directy
        """
        with np.errstate(divide="ignore", invalid="ignore"):  # suppress div by 0 errors
            spectrum, freqs, t, im = plt.specgram(
                self.scipy_wav_data, Fs=self.rate, NFFT=1024
            )
            self.specgramDataTuple = (spectrum, freqs, t, im)

    def computeSpectrumData(self):
        """
        Compute spectrum data for low, mid, high frequencies \n
        Returns a tuple containing 3 tuples, where each tuple contains two values: the frequency index, and numpy array of spectrum data

        @returns
            spectrumData_per_frequencyIndex: \n
            (
                (lowFreqIndex, lowFreqSpectrumData),\n
                (midFreqIndex, midFreqSpectrumData),\n
                (highFreqIndex, highFreqSpectrumData),
            )
        """
        frequencies = (250, 1000, 5000)  # (low, mid, high)

        self.computeSpecgram()
        spectrum, freqs, t, im = self.specgramDataTuple

        frequencyIndices = tuple(map(lambda freq: np.argmax(freqs > freq), frequencies))
        with np.errstate(divide="ignore", invalid="ignore"):  # suppress div by 0 errors
            spectrumsTuple = tuple(
                map(lambda index: 10 * np.log10(spectrum[index]), frequencyIndices)
                # map(lambda index: spectrum[index], frequencyIndices)
            )
        spectrumData_per_frequencyIndex = tuple(zip(frequencyIndices, spectrumsTuple))
        return spectrumData_per_frequencyIndex

    def computeRT20(self):
        """
        Computes RT60 for low, mid, high frequency \n
        Returns a tuple containing 3 tuples, where each tuple contains 3 values: the frequency index, ordered pair of max time and db value, and ordered pair of time and db value -25

        @returns
            rt60_per_freq: \n
            (
                (lowFreqIndex, lowFreq_maxVal_orderedPair, lowFreq_maxVal_m25_orderedPair),\n
                (midFreqIndex, midFreq_maxVal_orderedPair, midFreq_maxVal_m25_orderedPair),\n
                (highFreqIndex, highFreq_maxVal_orderedPair, highFreq_maxVal_m25_orderedPair),
            )
        """
        (
            (lowFreqIndex, lowSpec),
            (midFreqIndex, midSpec),
            (highFreqIndex, highSpec),
        ) = self.computeSpectrumData()
        plt.clf()
        spectrum, freqs, t, im = self.specgramDataTuple

        maxdbVals = tuple(
            map(lambda npArr: npArr[np.argmax(npArr)], (lowSpec, midSpec, highSpec))
        )
        raw_maxdbVals_m20 = tuple(np.array(maxdbVals) - 20)

        """Offsetting by 5dB causes bad calculations..."""
        # maxVals = tuple(np.array(maxVals) - 5)
        # maxVals_m25 = tuple(np.array(maxVals) - 25)

        maxVals_ind = tuple(
            map(lambda npArr: np.argmax(npArr), (lowSpec, midSpec, highSpec))
        )

        maxVals_m20_ind = tuple(
            map(
                lambda tup: np.argmin(np.abs(tup[1] - tup[0])),
                tuple(
                    zip(
                        raw_maxdbVals_m20,
                        (
                            lowSpec[maxVals_ind[0] :],
                            midSpec[maxVals_ind[1] :],
                            highSpec[maxVals_ind[2] :],
                        ),
                    )
                ),
            )
        )
        maxVals_m20_ind = tuple(np.array(maxVals_ind) + np.array(maxVals_m20_ind))

        actual_maxdbVals_m20 = (
            lowSpec[maxVals_m20_ind[0]],
            midSpec[maxVals_m20_ind[1]],
            highSpec[maxVals_m20_ind[2]],
        )

        time_maxVals = np.array(tuple(map(lambda ind: t[ind], maxVals_ind)))
        time_maxVals_m20 = np.array(tuple(map(lambda ind: t[ind], maxVals_m20_ind)))

        tup_time_maxVals = tuple(time_maxVals)
        tup_time_maxVals_m20 = tuple(time_maxVals_m20)

        maxVals_orderedPair = tuple(zip(tup_time_maxVals, maxdbVals))  # (time, db)
        maxVals_m25_orderedPair = tuple(zip(tup_time_maxVals_m20, actual_maxdbVals_m20))

        # rt60 = tuple(3 * (time_maxVals_m20 - time_maxVals))
        rt20_per_freqIndex = tuple(
            zip(
                (lowFreqIndex, midFreqIndex, highFreqIndex),
                maxVals_orderedPair,
                maxVals_m25_orderedPair,
            )
        )
        # print("rt60", rt20_per_freqIndex)
        return rt20_per_freqIndex
    
    def computeResonantFreq(self) -> float:
        self.computeSpecgram()
        plt.clf()
        spectrum, freq, t, im = self.specgramDataTuple
        crunched = np.array(tuple(map((lambda row: np.mean(row)), spectrum)))

        return freq[np.argmax(crunched)]


# EXAMPLE
'''
DUMMY_PATH = "media/Clap.m4a"  # path to audio file. edit to reflect your own audio file



# first... proccess the inputted audio file
audiofile = ProcessAudio(DUMMY_PATH)
audiofile.exportAsWav()  # convert to wav
print(audiofile.destinationPath)  # shows that wav is exported to new destination

# next... use the wav file to compute all the needed data
c = ComputeAudio(audiofile.destinationPath)  # get wav from its new destination
resonantFreq = c.computeResonantFreq()
print(f'The resonant freq is {resonantFreq}Hz')

(
    (lowFreqIndex, lowFreqSpecData),
    (midFreqIndex, midFreqSpecData),
    (highFreqIndex, highFreqSpecData),
) = (
    c.computeSpectrumData()
)  # call this method to get all the necessary data to plot graphs for all 3 frequencies

(
    spectrum,
    freqs,
    times,
    im,
) = c.specgramDataTuple  # call this propery to get necessary data for later use

# call this method to get all the necessary data to display RT60 for all 3 frequencies, RT60 needs to be calculated. orderedPairs give time values to calculate RT20 and mark points on graphs. multiply RT20 by 3 to get RT60
# ordered pairs are (time, dbVal)
(
    (lowFreqIndex, lowFreq_maxVal_orderedPair, lowFreq_maxVal_m25_orderedPair),
    (midFreqIndex, midFreq_maxVal_orderedPair, midFreq_maxVal_m25_orderedPair),
    (highFreqIndex, highFreq_maxVal_orderedPair, highFreq_maxVal_m25_orderedPair),
) = c.computeRT20()
# NOTE: low/mid/highFreqIndex names shadow the names above (from c.computeSpectrumData()). this should be fine since they are exactly the same values


# using the values...

# plot raw waveform
raw_data = c.scipy_wav_data
length = c.audioLength
t_axis = np.linspace(0, length, raw_data.shape[0])
plt.plot(t_axis, raw_data)
plt.title("Raw Waveform")
plt.show()

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

# plot all 3 freqs on one graph
plt.plot(times, lowFreqSpecData, label="low")
plt.plot(times, midFreqSpecData, label="mid")
plt.plot(times, highFreqSpecData, label="high")
plt.legend() # required to differentiate between graphs
plt.title("Combined")
plt.show()

# computing avg rt60 and difference from 0.5sec
avg_rt60 = (lowFreqRT60 + midFreqRT60 + highFreqRT60) / 3

difference = avg_rt60 - 0.5

print(f"Avg rt60 = {avg_rt60}. Difference from 0.5sec = {difference}")

# additional plot will be the specgram
c.computeSpectrumData()
plt.show()
'''
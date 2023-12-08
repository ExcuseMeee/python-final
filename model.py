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

    def cleanAudio(self) -> AudioSegment | None:
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
        '''
        Helper method, do not call directy 
        '''
        with np.errstate(divide="ignore", invalid="ignore"):  # suppress div by 0 errors
            spectrum, freqs, t, im = plt.specgram(
                self.scipy_wav_data, Fs=self.rate, NFFT=1024
            )
            self.specgramDataTuple = (spectrum, freqs, t, im)
        plt.clf()

    def computeSpectrumData(self):
        '''
        Compute spectrum data for low, mid, high frequencies \n
        Returns a tuple containing 3 tuples, where each tuple contains two values: the frequency index, and numpy array of spectrum data

        @returns
            spectrumData_per_frequencyIndex: \n
            (
                (lowFreqIndex, lowFreqSpectrumData),\n
                (midFreqIndex, midFreqSpectrumData),\n
                (highFreqIndex, highFreqSpectrumData),
            )
        '''
        frequencies = (250, 1000, 5000)  # (low, mid, high)

        self.computeSpecgram()
        spectrum, freqs, t, im = self.specgramDataTuple

        frequencyIndices = tuple(map(lambda freq: np.argmax(freqs > freq), frequencies))
        with np.errstate(divide="ignore", invalid="ignore"):  # suppress div by 0 errors
            spectrumsTuple = tuple(
                map(lambda index: 100 * np.log10(spectrum[index]), frequencyIndices)
                # map(lambda index: spectrum[index], frequencyIndices)
            )
        spectrumData_per_frequencyIndex = tuple(zip(frequencyIndices, spectrumsTuple))
        return spectrumData_per_frequencyIndex

    def computeRT60(self):
        '''
        Computes RT60 for low, mid, high frequency \n
        Returns a tuple containing 3 tuples, where each tuple contains two values: the frequency index and rt60 value

        @returns
            rt60_per_freq: \n
            (
                (lowFreqIndex, lowFreqRT60),\n
                (midFreqIndex, midFreqRT60),\n
                (highFreqIndex, highFreqRT60),
            )
        '''
        (
            (lowFreqIndex, lowSpec),
            (midFreqIndex, midSpec),
            (highFreqIndex, highSpec),
        ) = self.computeSpectrumData()
        spectrum, freqs, t, im = self.specgramDataTuple
        maxVals = tuple(
            map(lambda npArr: npArr[np.argmax(npArr)], (lowSpec, midSpec, highSpec))
        )

        """Offsetting by 5dB causes bad calculations..."""
        # maxVals_m5 = tuple(np.array(maxVals) - 5)
        # maxVals_m25 = tuple(np.array(maxVals) - 25)

        maxVals_m20 = tuple(np.array(maxVals) - 20)

        maxVals_ind = tuple(
            map(
                lambda tup: np.argmin(np.abs(tup[1] - tup[0])),
                tuple(zip(maxVals, (lowSpec, midSpec, highSpec))),
            )
        )
        maxVals_m20_ind = tuple(
            map(
                lambda tup: np.argmin(np.abs(tup[1] - tup[0])),
                tuple(
                    zip(
                        maxVals_m20,
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

        time_maxVals = np.array(tuple(map(lambda ind: t[ind], maxVals_ind)))
        time_maxVals_m20 = np.array(tuple(map(lambda ind: t[ind], maxVals_m20_ind)))

        rt60 = tuple(3 * (time_maxVals_m20 - time_maxVals))
        rt60_per_freqIndex = tuple(
            zip((lowFreqIndex, midFreqIndex, highFreqIndex), rt60)
        )
        return rt60_per_freqIndex


#EXAMPLE

DUMMY_PATH = "media/Clap.m4a"  # path to audio file. edit to reflect your own audio file

# first... proccess the inputted audio file
audiofile = ProcessAudio(DUMMY_PATH)
audiofile.exportAsWav() # convert to wav
print(audiofile.destinationPath) # shows that wav is exported to new destination

# next... use the wav file to compute all the needed data
c = ComputeAudio(audiofile.destinationPath) # get wav from its new destination

(
    (lowFreqIndex, lowFreqSpecData),
    (midFreqIndex, midFreqSpecData),
    (highFreqIndex, highFreqSpecData),
) = c.computeSpectrumData() # call this method to get all the necessary data to plot graphs for all 3 frequencies

spectrum, freqs, times, im = c.specgramDataTuple # call this propery to get necessary data for later use

(
    (lowFreqIndex, lowFreqRT60),
    (midFreqIndex, midFreqRT60),
    (highFreqIndex, highFreqRT60),
) = c.computeRT60() # call this method to get all the necessary data to display RT60 for all 3 frequencies
# NOTE: low/mid/highFreqIndex names shadow the names above (from c.computeSpectrumData()). this should be fine since they are exactly the same values


# using the values...

# # low frequency
# print(f'The RT60 for low frequency ({freqs[lowFreqIndex]}Hz) is {lowFreqRT60} sec')
# plt.plot(times, lowFreqSpecData) 
# plt.title(f'Plot of Intensity vs Time for {freqs[lowFreqIndex]}Hz frequency')
# plt.xlabel("Time (s)")
# plt.ylabel("Intensity (dB)")
# plt.show()

# mid frequency
print(f'The RT60 for mid frequency ({freqs[midFreqIndex]}Hz) is {midFreqRT60} sec')
plt.plot(times, midFreqSpecData) 
plt.title(f'Plot of Intensity vs Time for {freqs[midFreqIndex]}Hz frequency')
plt.xlabel("Time (s)")
plt.ylabel("Intensity (dB)")
plt.show()

# # high frequency
# print(f'The RT60 for high frequency ({freqs[highFreqIndex]}Hz) is {highFreqRT60} sec')
# plt.plot(times, highFreqSpecData) 
# plt.title(f'Plot of Intensity vs Time for {freqs[highFreqIndex]}Hz frequency')
# plt.xlabel("Time (s)")
# plt.ylabel("Intensity (dB)")
# plt.show()
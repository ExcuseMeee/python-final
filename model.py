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
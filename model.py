from pathlib import Path
from pydub import AudioSegment
import os
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np

DUMMY_PATH = "media/Clap.m4a"


class ProcessAudio:
    def __init__(self, filePath: str) -> None:
        """
        Create ProcessAudio object
        @params
            filePath: path to file, str

        @Object
            Members:
                validFileTypes: valid file types, list
                filePath: original path to file, str
                fileType: file extension, str
                isValid: is file a valid type, bool
                destinationPath: path to exported wav file
            Methods:
                exportAsWav()
        """
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
        self.dataForFrequencies = ()

    def computeSpecgram(self):
        with np.errstate(divide="ignore", invalid="ignore"):  # suppress div by 0 errors
            spectrum, freqs, t, im = plt.specgram(
                self.scipy_wav_data, Fs=self.rate, NFFT=1024
            )
            self.specgramDataTuple = (spectrum, freqs, t, im)

    def computeSpectrumData(self):
        frequencies = (20, 1000, 7000)  # (low, mid, high)

        self.computeSpecgram()
        spectrum, freqs, t, im = self.specgramDataTuple

        frequencyIndices = tuple(map(lambda freq: np.argmax(freqs > freq), frequencies))
        with np.errstate(divide="ignore", invalid="ignore"): # suppress div by 0 errors
            spectrumsTuple = tuple(
                map(lambda index: 100 * np.log10(spectrum[index]), frequencyIndices)
            )
        spectrumData_per_frequencyIndex = tuple(zip(frequencyIndices, spectrumsTuple))
        return spectrumData_per_frequencyIndex

    def computeRT60(self):
        (
            (lowFreqIndex, lowSpec),
            (midFreqIndex, midSpec),
            (highFreqIndex, highSpec),
        ) = self.computeSpectrumData()
        spectrum, freqs, t, im = self.specgramDataTuple
        print(midSpec)
        maxValsIndex = tuple(map(lambda npArr: np.argmax(npArr), (lowSpec, midSpec, highSpec)))
        # print(maxValsIndex)


audio1 = ProcessAudio(DUMMY_PATH)
audio1.exportAsWav()
print(audio1.destinationPath)

c = ComputeAudio(audio1.destinationPath)
# data = c.computeSpectrumData()
c.computeRT60()
# print(data)
# plt.show()
# plt.specgram(c.scipy_wav_data, Fs= c.rate, NFFT=256)
# plt.colorbar()
# plt.show()

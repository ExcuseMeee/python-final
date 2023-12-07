from pathlib import Path
from pydub import AudioSegment
import os

DUMMY_PATH = "media/16bit2chan.wav"

class ProcessAudio:
    
    def __init__(self, filePath: str) -> None:
        '''
        Create ProcessAudio object
        @params
            filePath: path to file, str
    
        @Object
            Members:
                validFileTypes: valid file types, list
                filePath: original path to file, str
                fileType: file extension, str
                isValid(: is file a valid type, bool
            Methods:
                exportAsWav()
        '''
        self.validFileTypes = [".wav", ".m4a", ".mp3"]
        self.filePath = filePath
        self.fileType = Path(filePath).suffix
        
        self.isValid = self.fileType in self.validFileTypes

    def cleanAudio(self) -> AudioSegment | None:
        '''
        Helper Method, do not call directly
        '''
        if not self.isValid: return

        format = (self.fileType)[1:]

        rawAudio: AudioSegment = AudioSegment.from_file(self.filePath, format=format)
        monoAudio = rawAudio.set_channels(1)

        return monoAudio
    
    def exportAsWav(self):
        '''
        Export the current ProcessAudio object as wav file to media/ folder\n
        Will not export if fileType of object is not valid 
        '''
        monoAudio = self.cleanAudio()

        if not monoAudio: return

        if not os.path.exists("media"):
            os.mkdir("media")

        monoAudio.export("media/cleanedAudio.wav", format="wav")

audio1 = ProcessAudio(DUMMY_PATH)
audio1.exportAsWav()





# def validateFile(filePath: str):
#     '''
#     validFileTypes = [".wav", ".m4a", ".mp3"]
#     @params 
#         filePath(str): path to audio file
#     @returns
#         tuple[bool, str]: is file valid, file type 
#     '''
#     validFileTypes = [".wav", ".m4a", ".mp3"]
#     fileType = Path(filePath).suffix

#     return (
#         fileType in validFileTypes,
#         fileType
#     )

# def convertToWav(filePath: str):
#     '''
#     Converts valid files into wav format. Saves to media folder\n
#     Will not convert invalid file types.

#     @params
#         filePath(str): path to audio file
#     @returns
#         None
#     '''
#     isValid, fileType = validateFile(filePath)
    
#     if not isValid: return

#     monoAudio = cleanAudio(filePath, fileType)
#     print(monoAudio.channels)
#     if not os.path.exists("media"): 
#         os.mkdir("media")
    
#     monoAudio.export("media/cleanedAudio.wav", format="wav")


# def cleanAudio(filePath: str, fileType: str)-> AudioSegment:
#     '''
#     @params
#         filePath(str): path to audio file
#         fileType(str): file extension
#     @returns
#         1 channel AudioSegment
#     '''
#     format = fileType[1:]

#     rawAudio: AudioSegment = AudioSegment.from_file(filePath, format=format)
#     monoAudio = rawAudio.set_channels(1)

#     return monoAudio




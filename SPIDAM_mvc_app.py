from model import ProcessAudio
from model import ComputeAudio
from view import View
from controller import Controller
import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Audio Visualizer')


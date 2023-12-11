from model import ProcessAudio
from model import ComputeAudio
from view import View
from controller import Controller
import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Audio Visualizer')

        view = View()
        view.grid(row=0, column=0, padx=15, pady=15)

        controller = Controller(audio)

        view.set_controller(controller)

if __name__ == "__main__":
    app = App()
    app.mainloop()


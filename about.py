#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from aboutui import aboutClassUI


class aboutClass(aboutClassUI):
    def __init__(self, master=None):
        super().__init__(master)

    def btnQuit_Clicked(self):
        self.mainwindow.destroy()


if __name__ == "__main__":
    app = aboutClass()
    app.run()

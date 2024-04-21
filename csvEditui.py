#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "csvEdit.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class csvEditClassUI:
    def __init__(self, master=None):
        self.builder = pygubu.Builder()
        self.builder.add_resource_paths(RESOURCE_PATHS)
        self.builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: tk.Toplevel = self.builder.get_object(
            "toplevel1", master)
        # Main menu
        _main_menu = self.builder.get_object("mainMenu", self.mainwindow)
        self.mainwindow.configure(menu=_main_menu)
        self.builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def clicked_mnuCmdNew(self, itemid):
        pass

    def clicked_mnuCmdOpen(self):
        pass

    def clicked_mnuCmdSave(self):
        pass

    def clicked_mnuCmdSaveAs(self, itemid):
        pass

    def clicked_mnuCmdQuit(self):
        self.mainwindow.destroy()

    def clicked_mnuCmdAbout(self):
        pass


if __name__ == "__main__":
    app = csvEditClassUI()
    app.run()

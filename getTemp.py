#!/usr/bin/python3
import pathlib
import tkinter as tk
from tkinter import font as tkFont
import pygubu
from getTempui import getTempClassUI
from datetime import datetime


class getTempClass(getTempClassUI):
    def __init__(self, master=None):
        super().__init__(master)
        self.lblDateTime = self.builder.get_object("lblDateTime", self.mainwindow) 
        self.lblChannel_4 = self.builder.get_object("lblChannel_4", self.mainwindow) 
        self.lblChannel_1 = self.builder.get_object("lblChannel_1", self.mainwindow) 
        self.lblGo        = self.builder.get_object("lblGo", self.mainwindow) 
        self.lblChannel_4.configure(bg="white")
        self.lblChannel_1.configure(bg="white")
        self.port = "COM10"
        self.portOpen = False
        self.lblPortStatus = self.builder.get_object("lblPortStatus", self.mainwindow) 
        self.lblPortStatus.configure(text=f"port {self.port} is closed", bg="white")
        self.printDateTime()
        self.looping = False
        self.lblGo.bind("<Button-1>", self.lblGo_clicked)
        self.lblGo.bind("<ButtonRelease-1>", self.lblGo_released)
        self.lblGo.configure( bg="lightgray")

    def printDateTime(self):
        now = datetime.now()
        dateStr = now.strftime("%F %T")
        self.lblDateTime.configure(text=dateStr)

    def lblGo_released(self,event):
        self.lblGo.configure( bg="lightgray")

    def lblGo_clicked(self,event):
        self.lblGo.configure( bg="gray")
        if self.looping:
            self.looping = False
        else:
            self.mainwindow.after(1000,self.loop_stuff)
            self.looping = True

    def loop_stuff(self):
        if self.looping:
            self.printDateTime()
            if not self.portOpen:
                self.portOpen = True
                self.lblPortStatus.configure(text=f"port {self.port} is open", bg="white")
                self.lblGo.configure( text="STOP")
            today = datetime.now()
            if ( today.second%2 == 0):
                self.lblChannel_4.configure(bg="red")
            else:
                self.lblChannel_4.configure(bg="green")

            self.mainwindow.after(1000,self.loop_stuff)
        else:
            if self.portOpen:
                self.portOpen = False
                self.lblPortStatus.configure(text=f"port {self.port} is closed", bg="white")
                self.lblGo.configure(text="GO")
            self.lblChannel_4.configure(bg="white")
            self.lblChannel_1.configure(bg="white")
            

if __name__ == "__main__":
    app = getTempClass()
    app.run()

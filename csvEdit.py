#!/usr/bin/python3
import pathlib
import tkinter as tk
from tkinter import filedialog
import pygubu
from csvEditui import csvEditClassUI
import csv


class csvEditClass(csvEditClassUI):
    def __init__(self, master=None):
        super().__init__(master)       
        self.trvCSV: ttk.Treeview = self.builder.get_object("trvCSV", master)     
        self.csvFileName = ""

    def getCSVHeaders(self):
        headers = []
        for c in self.trvCSV.get_children():
            item = self.trvCSV.item(c)
            values = item["values"]
            for i in range(0,len(values)):
                headers.append(self.trvCSV.heading(i)["text"])
            break
        return headers       

    def saveCSVFile(self,filename):
        self.csvFileName = filename
        with open(self.csvFileName,'w') as csvFile:
            headers  = self.getCSVHeaders()
            csvWrite = csv.writer(csvFile)
            csvWrite.writerow(headers)
            for c in self.trvCSV.get_children():
                item = self.trvCSV.item(c)
                values = item["values"]
                csvWrite.writerow(values)          

    def clicked_mnuCmdSaveAs(self,itemid):   
        """
        """
        filename = filedialog.asksaveasfilename(
            title="Select a CSV File",
            filetypes=(
                ("csv files", "*.csv"),
                ("all files", "*.*")
            )            
        )
        if filename != "":
            self.saveCSVFile(filename)        
                    

    def clicked_mnuCmdSave(self):   
        """
        """
        self.saveCSVFile(self.csvFileName)

    def clicked_mnuCmdOpen(self):

        filename = filedialog.askopenfilename(
            title="Select a CSV File",
            filetypes=(
                ("csv files", "*.csv"),
                ("all files", "*.*")
            )
        )

        print(f"work with {self.csvFileName}")         
        if filename != "":
            self.csvFileName = filename
            self.trvCSV.delete(*self.trvCSV.get_children())              
            cnt = 1
            with open(self.csvFileName, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if ( cnt == 1 ):
                        keys =  list(row.keys())
                        self.trvCSV.configure( columns=keys )
                        for txt in keys:
                            self.trvCSV.heading(txt, text=txt)
                        
                    self.trvCSV.insert(
                        parent="",
                        index=tk.END,
                        text=str(cnt),
                        values=list(row.values())
                    )
                    cnt += 1
                        

if __name__ == "__main__":
    app = csvEditClass()
    app.run()

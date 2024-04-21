#!/usr/bin/python3
import pathlib
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pygubu
from csvEditui import csvEditClassUI
import csv


class csvEditClass(csvEditClassUI):
    def __init__(self, master=None):
        super().__init__(master)       
        self.trvCSV: ttk.Treeview = self.builder.get_object("trvCSV", master)     
        self.trvCSV.bind("<Double-1>",self.on_double_click)
        self.csvFileName = ""        
    
    def on_double_click(self,event):
        region_clicked = self.trvCSV.identify_region(
            x=event.x, 
            y=event.y
        )

        #was a cell clicked?
        if region_clicked not in ("cell"):
            return
        #what was double clicked?
        column = self.trvCSV.identify_column(event.x)
        column_index = int(column[1:]) - 1

        selected_iid = self.trvCSV.focus()  
        selected_values = self.trvCSV.item(selected_iid)  

        if column == "#0":
            selected_text = selected_values.get("text")
        else: 
            selected_text = selected_values.get("values")[column_index]
        print(selected_text)

        #get boundry of cell to edit
        (boxX, boxY, boxW, boxH) = self.trvCSV.bbox(selected_iid, column)

        self.mainwindow.entry_edit = ttk.Entry(
            self.mainwindow,
            width=boxW
        )
        self.mainwindow.entry_edit.editing_column_index = column_index
        self.mainwindow.entry_edit.editing_item_iid     = selected_iid
        self.mainwindow.entry_edit.place(
                x=boxX, 
                y=boxY,
                w=boxW,
                h=boxH
        )
        self.mainwindow.entry_edit.insert(0,selected_text)
        self.mainwindow.entry_edit.select_range(0,tk.END)
        self.mainwindow.entry_edit.focus()
        
        self.mainwindow.entry_edit.bind("<FocusOut>", self.on_focus_out)
        self.mainwindow.entry_edit.bind("<Return>", self.on_enter_pressed)        
   
    def on_enter_pressed(self,event):
        new_text = event.widget.get()
        selected_iid = event.widget.editing_item_iid
        column_index = event.widget.editing_column_index

        if ( column_index == -1): #tree column
            self.item(selected_iid, text=new_text)
        else:
            current_values = self.trvCSV.item(selected_iid).get("values")
            current_values[column_index] = new_text
            self.trvCSV.item(selected_iid, value=current_values)
        event.widget.destroy()



    def on_focus_out(self,event):
        event.widget.destroy()



    def getTreeHeaders(self):
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
            headers  = self.getTreeHeaders()
            csvWrite = csv.writer(csvFile)
            csvWrite.writerow(headers)
            for c in self.trvCSV.get_children():
                item = self.trvCSV.item(c)
                values = item["values"]
                csvWrite.writerow(values)          

    def clicked_mnuCmdSaveAs(self,itemid):   
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

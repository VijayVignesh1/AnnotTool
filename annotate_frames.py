import cv2
from PIL import Image,ImageTk
from PIL import ImageTk as itk
import tkinter as tk
from tkinter import ttk
import glob
import os
import csv
from tkinter import filedialog

from points_annotation import PointAnnotate
from rectangles_annotation import RectangleAnnotate

class initialDialogue(tk.Frame):
    """Illustrate how to drag items on a Tkinter canvas"""

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root=root
        self.foldername=""
        self.folder=tk.StringVar()
        csvfile=ttk.Label(self.root, text="File").grid(row=1, column=0)
        bar=ttk.Entry(self.root, textvariable=self.folder).grid(row=1, column=1) 
        self.is_quit=0

        # Place buttons in place
        self.bbutton= ttk.Button(self.root, text="Browse", command=self.browse)
        self.bbutton.grid(row=1, column=3)
        label=ttk.Label(self.root, text="Point/Rectangle")
        label.place(x=0,y=35)
        self.v0=tk.IntVar()
        self.v0.set(1)
        r1=tk.Radiobutton(self.root, text="Point", variable=self.v0,value=1)
        r2=tk.Radiobutton(self.root, text="Rectangle", variable=self.v0,value=2)
        r1.place(x=100,y=35)
        r2.place(x=165, y=35)
        ok_button=ttk.Button(self.root, text="OK", command=self.submit)
        ok_button.place(x=150,y=70)
        quit_button=ttk.Button(self.root, text="Quit", command=self.quit)
        quit_button.place(x=20,y=70)

    def submit(self):
        """ Get the input from the user and load the proper class """
        self.foldername=self.folder.get()
        self.point=self.v0.get()
        self.root.destroy()

    def browse(self):
        """ Browse to open the image in a particular directory """ 
        self.foldername = filedialog.askdirectory()
        self.folder.set(self.foldername)

    def quit(self):
        self.is_quit=1
        self.root.destroy()


if __name__ == "__main__":
    root_init=tk.Tk()
    root_init.geometry('250x125')
    temp=initialDialogue(root_init)
    root_init.mainloop()
    if not temp.is_quit:
        if temp.point==1:
            images_folder=temp.foldername+'/'
            root_point = tk.Tk()
            root_point.title("Image Scanner")
            PointAnnotate(root_point,images_folder).pack(fill="both", expand=True)
            root_point.mainloop()
        if temp.point==2:
            images_folder=temp.foldername+'/'
            root_point = tk.Tk()
            root_point.title("Image Scanner")
            RectangleAnnotate(root_point,images_folder).pack(fill="both", expand=True)
            root_point.mainloop()

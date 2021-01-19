import cv2
import imutils
from PIL import ImageTk as itk
from PIL import Image
import tkinter as tk
from tkinter import ttk
import glob
import os
import csv

class PointAnnotate(tk.Frame):
    """ Capture points by means of mouse click, navigate through the directory and save the final data as csv """

    def __init__(self, parent,images_folder):
        tk.Frame.__init__(self, parent)
        self.parent=parent
        self.images_folder=images_folder
        self.images=glob.glob(self.images_folder+"*.jpg")

        self.current_index=0
        
        self.annotation_dict={}

        self.img = cv2.imread(self.images[0])
        self.img = cv2.resize(self.img,(500,500))

        # create a canvas
        self.canvas = tk.Canvas(width=self.img.shape[1]+100, height=self.img.shape[0])
        self.canvas.pack()

        self.img_tk = Image.fromarray(self.img)
        self.image = itk.PhotoImage(image=self.img_tk)

        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

        self._drag_data = {"x": 0, "y": 0, "item": None}
        self.point=None
        self.point_list=[]

        self.canvas.pack()

        # Add buttons and their functionality
        style = ttk.Style()
        style.configure('TButton', font = 
               ('calibri', 12, 'bold'), 
                    borderwidth = '4')
        style.map('TButton', foreground = [('active', 'green')], 
                     background = [('active', 'black')]) 
        B_next=ttk.Button(self.canvas,text="Next",command=self.nextImage)
        B_next.grid(row = 1, column = 3, pady = 10, padx = 10)

        B_back=ttk.Button(self.canvas,text="Back",command=self.previousImage)
        B_back.grid(row = 1, column = 3, pady = 10, padx = 10)
    
        B_save=ttk.Button(self.canvas,text="Save",command=self.saveData)
        B_save.grid(row = 1, column = 3, pady = 10, padx = 10)

        B_clear_last_point=ttk.Button(self.canvas,text="Clear",command=self.clearLastPoint)
        B_clear_last_point.grid(row = 1, column = 3, pady = 10, padx = 10)

        B_clear_all_points=ttk.Button(self.canvas,text="Clear All",command=self.clearAllPoints)
        B_clear_all_points.grid(row = 1, column = 3, pady = 10, padx = 10)

        B_quit=ttk.Button(self.canvas,text="Quit",command=self.quit)
        B_quit.grid(row = 1, column = 3, pady = 10, padx = 10)

        self.canvas.create_window(self.img.shape[1],self.img.shape[0]/2-150,anchor=tk.SW,window=B_next)
        self.canvas.create_window(self.img.shape[1],self.img.shape[0]/2-100,anchor=tk.SW,window=B_back)
        self.canvas.create_window(self.img.shape[1],self.img.shape[0]/2-50,anchor=tk.SW,window=B_save)
        self.canvas.create_window(self.img.shape[1],self.img.shape[0]/2,anchor=tk.SW,window=B_clear_last_point)
        self.canvas.create_window(self.img.shape[1],self.img.shape[0]/2+50,anchor=tk.SW,window=B_clear_all_points)
        self.canvas.create_window(self.img.shape[1],self.img.shape[0]/2+200,anchor=tk.SW,window=B_quit)

        # add bindings for clicking
        self.canvas.bind("<Button 1>", self.click)

    def saveData(self):
        """ Save all the captured points of all the images as a csv file under the appropriate headers """
        self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.point_list
        for i in self.images:
            key=os.path.basename(i)
            if key in self.annotation_dict.keys():
                list_point=self.annotation_dict[key]
            else:
                continue
            img=cv2.imread(i)
            for j in range(len(list_point)):
                self.annotation_dict[key][j][0]=int(list_point[j][0]*(img.shape[1]/500))
                self.annotation_dict[key][j][1]=int(list_point[j][1]*(img.shape[0]/500))
        save_output=self.images_folder+"/output.csv"
        with open(save_output, 'w', newline='') as csvfile:
            fieldnames = ['image', 'annotation']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for key in self.annotation_dict:
                writer.writerow({'image': key, 'annotation': self.annotation_dict[key]})
        self.parent.destroy()


    def nextImage(self):
        """ Go to the next image and display all the associated points captured for it """
        self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.point_list
        self.current_index=(self.current_index + 1) % len(self.images)
        self.img = cv2.imread(self.images[self.current_index])
        self.img = cv2.resize(self.img,(500,500))
        if os.path.basename(self.images[self.current_index]) in self.annotation_dict.keys():
            self.point_list=self.annotation_dict[os.path.basename(self.images[self.current_index])]
            for x,y in self.point_list:
                cv2.circle(self.img,(x,y),1,(255,0,0),3)
        else:
            self.point_list=[]
            self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.point_list
        self.img_tk = Image.fromarray(self.img)
        self.image = itk.PhotoImage(image=self.img_tk)
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW) 
 
        
    def previousImage(self):
        """ Go to the previous image and display all the associated points captured for it """
        self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.point_list
        self.current_index=(self.current_index - 1) % len(self.images)
        self.img = cv2.imread(self.images[self.current_index])
        self.img = cv2.resize(self.img,(500,500))

        if os.path.basename(self.images[self.current_index]) in self.annotation_dict.keys():
            self.point_list=self.annotation_dict[os.path.basename(self.images[self.current_index])]
            for x,y in self.point_list:
                cv2.circle(self.img,(x,y),1,(255,0,0),3)
        else:
            self.point_list=[]
            self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.point_list
        self.img_tk = Image.fromarray(self.img)
        self.image = itk.PhotoImage(image=self.img_tk)
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

    def clearLastPoint(self):
        """ Clear the most recently captured point for the given image """
        if len(self.point_list)>0:
            del self.point_list[-1]
        self.img = cv2.imread(self.images[self.current_index])
        self.img = cv2.resize(self.img,(500,500))
        if os.path.basename(self.images[self.current_index]) in self.annotation_dict.keys():
            self.point_list=self.annotation_dict[os.path.basename(self.images[self.current_index])]
            for x,y in self.point_list:
                cv2.circle(self.img,(x,y),1,(255,0,0),3)
        else:
            self.rect_list=[]
            self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.point_list  
        self.img_tk = Image.fromarray(self.img)
        self.image = itk.PhotoImage(image=self.img_tk)
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)   
         
    def clearAllPoints(self):
        """ Function to clear all the captured points for the given image"""
        if len(self.point_list)>0:
            self.point_list=[]
        self.img = cv2.imread(self.images[self.current_index])
        self.img = cv2.resize(self.img,(500,500))
        self.img_tk = Image.fromarray(self.img)
        self.image = itk.PhotoImage(image=self.img_tk)
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.point_list              

    def quit(self):
        self.parent.destroy()

    def click(self, event):
        """ Capture the clicking event and handle it """
        if event.x<500 and event.y<500:
            self.current_key=os.path.basename(self.images[self.current_index])
            self.point_list.append([event.x,event.y])
            self.img = cv2.imread(self.images[self.current_index])
            self.img = cv2.resize(self.img,(500,500))
            for x,y in self.point_list:
                self.img = cv2.circle(self.img,(x,y),1,(255,0,0),3)
            self.img_tk = Image.fromarray(self.img)
            self.image = itk.PhotoImage(image=self.img_tk)
            self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

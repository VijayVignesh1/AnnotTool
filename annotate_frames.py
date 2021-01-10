import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import threshold_local
import imutils
from PIL import Image,ImageTk
from PIL import ImageTk as itk
# from scan import *

import tkinter as tk     # python 3
from tkinter import ttk
import glob
import os
# import Tkinter as tk   # python 2
# from Edge_Detection import *
import csv
from tkinter import filedialog

class PointAnnotate(tk.Frame):
    """Illustrate how to drag items on a Tkinter canvas"""

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

        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        self.canvas.bind("<Button 1>", self.click)

    def saveData(self):
        self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.point_list
        for i in self.images:
            key=os.path.basename(i)
            if key in self.annotation_dict.keys():
                list_point=self.annotation_dict[key]
            else:
                continue
            img=cv2.imread(i)
            for j in range(len(list_point)):
                # self.annotation_dict[key][j][0]=int(list_rect[j][0]*(img.shape[1]/500))
                # self.annotation_dict[key][j][1]=int(list_rect[j][1]*(img.shape[0]/500))
                self.annotation_dict[key][j][0]=int(list_point[j][0]*(img.shape[1]/500))
                self.annotation_dict[key][j][1]=int(list_point[j][1]*(img.shape[0]/500))
                # img=cv2.rectangle(img,(self.annotation_dict[key][j][0],self.annotation_dict[key][j][1]),
                #                     (self.annotation_dict[key][j][2],self.annotation_dict[key][j][3]),(255,0,0),2)
        save_output=self.images_folder+"/output.csv"
        with open(save_output, 'w', newline='') as csvfile:
            fieldnames = ['image', 'annotation']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for key in self.annotation_dict:
                print(self.annotation_dict[key])
                writer.writerow({'image': key, 'annotation': self.annotation_dict[key]})
        self.parent.destroy()
    def nextImage(self):
        # print(self.annotation_dict)
        self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.point_list
        self.current_index=(self.current_index + 1) % len(self.images)
        self.img = cv2.imread(self.images[self.current_index])
        self.img = cv2.resize(self.img,(500,500))
        # print(os.path.basename(self.images[self.current_index]))
        if os.path.basename(self.images[self.current_index]) in self.annotation_dict.keys():
            # print(self.annotation_dict[os.path.basename(self.images[self.current_index])])
            # x=self.annotation_dict[os.path.basename(self.images[self.current_index])][0]
            # y=self.annotation_dict[os.path.basename(self.images[self.current_index])][1]
            # cv2.circle(self.img,(x,y),1,(255,0,0),3)
            self.point_list=self.annotation_dict[os.path.basename(self.images[self.current_index])]
            for x,y in self.point_list:
                # print(x1,y1,x2,y2)
                # self.rect=self.canvas.create_rectangle(x1,y1,x2,y2,fill="")
                cv2.circle(self.img,(x,y),1,(255,0,0),3)
        else:
            self.point_list=[]
            self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.point_list
        self.img_tk = Image.fromarray(self.img)
        self.image = itk.PhotoImage(image=self.img_tk)
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW) 
 
        
    def previousImage(self):
        # print(self.annotation_dict)
        self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.point_list
        self.current_index=(self.current_index - 1) % len(self.images)
        self.img = cv2.imread(self.images[self.current_index])
        self.img = cv2.resize(self.img,(500,500))

        if os.path.basename(self.images[self.current_index]) in self.annotation_dict.keys():
            # print(self.annotation_dict[os.path.basename(self.images[self.current_index])])
            # x=self.annotation_dict[os.path.basename(self.images[self.current_index])][0]
            # y=self.annotation_dict[os.path.basename(self.images[self.current_index])][1]
            # cv2.circle(self.img,(x,y),1,(255,0,0),3)
            self.point_list=self.annotation_dict[os.path.basename(self.images[self.current_index])]
            for x,y in self.point_list:
                # self.rect=self.canvas.create_rectangle(i[0],i[1],i[2],i[3],fill="")
                cv2.circle(self.img,(x,y),1,(255,0,0),3)
        else:
            self.point_list=[]
            self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.point_list
        self.img_tk = Image.fromarray(self.img)
        self.image = itk.PhotoImage(image=self.img_tk)
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

    def clearLastPoint(self):
        if len(self.point_list)>0:
            del self.point_list[-1]
        self.img = cv2.imread(self.images[self.current_index])
        self.img = cv2.resize(self.img,(500,500))
        if os.path.basename(self.images[self.current_index]) in self.annotation_dict.keys():
            # print(self.annotation_dict[os.path.basename(self.images[self.current_index])])
            # x=self.annotation_dict[os.path.basename(self.images[self.current_index])][0]
            # y=self.annotation_dict[os.path.basename(self.images[self.current_index])][1]
            # cv2.circle(self.img,(x,y),1,(255,0,0),3)
            self.point_list=self.annotation_dict[os.path.basename(self.images[self.current_index])]
            for x,y in self.point_list:
                # self.rect=self.canvas.create_rectangle(i[0],i[1],i[2],i[3],fill="")
                cv2.circle(self.img,(x,y),1,(255,0,0),3)
        else:
            self.rect_list=[]
            self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.point_list  
        self.img_tk = Image.fromarray(self.img)
        self.image = itk.PhotoImage(image=self.img_tk)
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)            
    def clearAllPoints(self):
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
        if event.x<500 and event.y<500:
            self.current_key=os.path.basename(self.images[self.current_index])
            self.point_list.append([event.x,event.y])
            # self.annotation_dict[self.current_key]=[event.x,event.y]
            # x=self.point_list[-1][0]
            # y=self.point_list[-1][1]
            
            self.img = cv2.imread(self.images[self.current_index])
            self.img = cv2.resize(self.img,(500,500))
            for x,y in self.point_list:
                self.img = cv2.circle(self.img,(x,y),1,(255,0,0),3)
            self.img_tk = Image.fromarray(self.img)
            self.image = itk.PhotoImage(image=self.img_tk)
            self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
            # print(event.x, event.y)
            # img=cv2.imread(self.images[self.current_index])
            # x_img=int(x*(img.shape[1]/500))
            # y_img=int(y*(img.shape[0]/500))
            # print(x_img,y_img)
            
class PointAnnotation(tk.Frame):
    """Illustrate how to drag items on a Tkinter canvas"""

    def __init__(self, parent,images_folder):
        tk.Frame.__init__(self, parent)

        self.parent=parent
        self.images_folder=images_folder
        self.images=glob.glob(self.images_folder+"*.jpg")

        self.current_index=0
        
        self.annotation_dict={}
        self.img = cv2.imread(self.images[0])

        self.img = cv2.resize(self.img,(500,500))
        
        self.canvas = tk.Canvas(width=self.img.shape[1]+100, height=self.img.shape[0])

        self.canvas.pack()

        self.img_tk = Image.fromarray(self.img)
        self.image = itk.PhotoImage(image=self.img_tk)


        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

        self.canvas.pack()
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

        B_quit=ttk.Button(self.canvas,text="Quit",command=self.quit)
        B_quit.grid(row = 1, column = 3, pady = 10, padx = 10)

        self.canvas.create_window(self.img.shape[1],self.img.shape[0]/2-50,anchor=tk.SW,window=B_next)
        self.canvas.create_window(self.img.shape[1],self.img.shape[0]/2,anchor=tk.SW,window=B_back)
        self.canvas.create_window(self.img.shape[1],self.img.shape[0]/2+50,anchor=tk.SW,window=B_save)
        self.canvas.create_window(self.img.shape[1],self.img.shape[0]/2+200,anchor=tk.SW,window=B_quit)

        self.canvas.bind("<Button 1>", self.click)

    def saveData(self):
        for i in self.images:
            key=os.path.basename(i)
            if key in self.annotation_dict.keys():
                x=self.annotation_dict[key][0]
                y=self.annotation_dict[key][1]
            else:
                continue
            img=cv2.imread(i)
            self.annotation_dict[key][0]=int(x*(img.shape[1]/500))
            self.annotation_dict[key][1]=int(y*(img.shape[0]/500))
        save_output=self.images_folder+"/output.csv"
        with open(save_output, 'w', newline='') as csvfile:
            fieldnames = ['image', 'annotation']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for key in self.annotation_dict:
                writer.writerow({'image': key, 'annotation': self.annotation_dict[key]})
        self.parent.destroy()
    def nextImage(self):
        self.current_index=(self.current_index + 1) % len(self.images)
        self.img = cv2.imread(self.images[self.current_index])
        self.img = cv2.resize(self.img,(500,500))
        if os.path.basename(self.images[self.current_index]) in self.annotation_dict:
            x=self.annotation_dict[os.path.basename(self.images[self.current_index])][0]
            y=self.annotation_dict[os.path.basename(self.images[self.current_index])][1]
            cv2.circle(self.img,(x,y),1,(255,0,0),3)
        self.img_tk = Image.fromarray(self.img)
        self.image = itk.PhotoImage(image=self.img_tk)
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)  
    def previousImage(self):
        self.current_index=(self.current_index - 1) % len(self.images)
        self.img = cv2.imread(self.images[self.current_index])
        self.img = cv2.resize(self.img,(500,500))
        if os.path.basename(self.images[self.current_index]) in self.annotation_dict:
            x=self.annotation_dict[os.path.basename(self.images[self.current_index])][0]
            y=self.annotation_dict[os.path.basename(self.images[self.current_index])][1]
            cv2.circle(self.img,(x,y),1,(255,0,0),3)
        self.img_tk = Image.fromarray(self.img)
        self.image = itk.PhotoImage(image=self.img_tk)
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)        
    def click(self, event):
        if event.x<500 and event.y<500:
            self.current_key=os.path.basename(self.images[self.current_index])
            self.annotation_dict[self.current_key]=[event.x,event.y]
            x=self.annotation_dict[os.path.basename(self.images[self.current_index])][0]
            y=self.annotation_dict[os.path.basename(self.images[self.current_index])][1]
            # print(x,y)
            self.img = cv2.imread(self.images[self.current_index])
            self.img = cv2.resize(self.img,(500,500))
            self.img=cv2.circle(self.img,(x,y),1,(255,0,0),3)
            self.img_tk = Image.fromarray(self.img)
            self.image = itk.PhotoImage(image=self.img_tk)
            self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
            # print(event.x, event.y)
            img=cv2.imread(self.images[self.current_index])
            x_img=int(x*(img.shape[1]/500))
            y_img=int(y*(img.shape[0]/500))
            # print(x_img,y_img)

    def quit(self):
        self.parent.destroy()

class initialDialogue(tk.Frame):
    """Illustrate how to drag items on a Tkinter canvas"""

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        """
        self.canvas = tk.Canvas(width=500, height=500)
        self.canvas.pack()
        B_next=ttk.Button(self.canvas,text="Next",command=self.scan)
        B_next.grid(row = 1, column = 3, pady = 10, padx = 10)

        B_back=ttk.Button(self.canvas,text="Back",command=self.scan)
        B_back.grid(row = 1, column = 3, pady = 10, padx = 10)
    
        B_save=ttk.Button(self.canvas,text="Save",command=self.scan)
        B_save.grid(row = 1, column = 3, pady = 10, padx = 10)

        self.canvas.create_window(10,10,anchor=tk.SW,window=B_next)
        self.canvas.create_window(10,40,anchor=tk.SW,window=B_back)
        self.canvas.create_window(10,70,anchor=tk.SW,window=B_save)
        """
        self.root=root
        self.foldername=""
        self.folder=tk.StringVar()
        csvfile=ttk.Label(self.root, text="File").grid(row=1, column=0)
        bar=ttk.Entry(self.root, textvariable=self.folder).grid(row=1, column=1) 
        # bar.insert(0,'asda')
        #Buttons  
        y=7
        # self.cbutton= ttk.Button(root, text="OK", command=self.scan)
        y+=1
        self.is_quit=0
        # self.cbutton.grid(row=10, column=3, sticky = tk.W + tk.E)
        self.bbutton= ttk.Button(self.root, text="Browse", command=self.browse)
        self.bbutton.grid(row=1, column=3)
        # root.mainloop()
        # self.txt_frame = tk.Frame(self)
        # self.txt_frame.grid(row=5, column=5)
        # self.txt_box = tk.Text(self.txt_frame, width=40, height=15)
        # self.txt_box.pack()
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
        self.foldername=self.folder.get()
        self.point=self.v0.get()
        # print(self.foldername)
        self.root.destroy()
    def browse(self):
        # Tk().withdraw() 
        self.foldername = filedialog.askdirectory()
        self.folder.set(self.foldername)
    def quit(self):
        self.is_quit=1
        self.root.destroy()

class RectangleAnnotate(tk.Frame):
    """Illustrate how to drag items on a Tkinter canvas"""

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
        self.start=[-1,-1]
        self.rect=None
        self.rect_list=[]

        self.canvas.pack()
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

        B_clear_last_rect=ttk.Button(self.canvas,text="Clear",command=self.clearLastRect)
        B_clear_last_rect.grid(row = 1, column = 3, pady = 10, padx = 10)

        B_clear_all_rect=ttk.Button(self.canvas,text="Clear All",command=self.clearAllRect)
        B_clear_all_rect.grid(row = 1, column = 3, pady = 10, padx = 10)

        B_quit=ttk.Button(self.canvas,text="Quit",command=self.quit)
        B_quit.grid(row = 1, column = 3, pady = 10, padx = 10)

        self.canvas.create_window(self.img.shape[1],self.img.shape[0]/2-150,anchor=tk.SW,window=B_next)
        self.canvas.create_window(self.img.shape[1],self.img.shape[0]/2-100,anchor=tk.SW,window=B_back)
        self.canvas.create_window(self.img.shape[1],self.img.shape[0]/2-50,anchor=tk.SW,window=B_save)
        self.canvas.create_window(self.img.shape[1],self.img.shape[0]/2,anchor=tk.SW,window=B_clear_last_rect)
        self.canvas.create_window(self.img.shape[1],self.img.shape[0]/2+50,anchor=tk.SW,window=B_clear_all_rect)
        self.canvas.create_window(self.img.shape[1],self.img.shape[0]/2+200,anchor=tk.SW,window=B_quit)

        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        self.canvas.bind("<ButtonPress-1>", self.drag_start)
        self.canvas.bind("<ButtonRelease-1>", self.drag_stop)
        self.canvas.bind("<B1-Motion>", self.drag)
    def saveData(self):
        self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.rect_list
        for i in self.images:
            key=os.path.basename(i)
            if key in self.annotation_dict.keys():
                list_rect=self.annotation_dict[key]
            else:
                continue
            img=cv2.imread(i)
            for j in range(len(list_rect)):
                self.annotation_dict[key][j][0]=int(list_rect[j][0]*(img.shape[1]/500))
                self.annotation_dict[key][j][1]=int(list_rect[j][1]*(img.shape[0]/500))
                self.annotation_dict[key][j][2]=int(list_rect[j][2]*(img.shape[1]/500))
                self.annotation_dict[key][j][3]=int(list_rect[j][3]*(img.shape[0]/500))
                img=cv2.rectangle(img,(self.annotation_dict[key][j][0],self.annotation_dict[key][j][1]),
                                    (self.annotation_dict[key][j][2],self.annotation_dict[key][j][3]),(255,0,0),2)
        save_output=self.images_folder+"/output.csv"
        with open(save_output, 'w', newline='') as csvfile:
            fieldnames = ['image', 'annotation']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for key in self.annotation_dict:
                writer.writerow({'image': key, 'annotation': self.annotation_dict[key]})
        self.parent.destroy()
    def nextImage(self):
        # print(self.annotation_dict)
        self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.rect_list
        self.current_index=(self.current_index + 1) % len(self.images)
        self.img = cv2.imread(self.images[self.current_index])
        self.img = cv2.resize(self.img,(500,500))
        self.img_tk = Image.fromarray(self.img)
        self.image = itk.PhotoImage(image=self.img_tk)
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW) 
        # print(os.path.basename(self.images[self.current_index]))
        if os.path.basename(self.images[self.current_index]) in self.annotation_dict.keys():
            # print(self.annotation_dict[os.path.basename(self.images[self.current_index])])
            # x=self.annotation_dict[os.path.basename(self.images[self.current_index])][0]
            # y=self.annotation_dict[os.path.basename(self.images[self.current_index])][1]
            # cv2.circle(self.img,(x,y),1,(255,0,0),3)
            self.rect_list=self.annotation_dict[os.path.basename(self.images[self.current_index])]
            for x1,y1,x2,y2 in self.rect_list:
                # print(x1,y1,x2,y2)
                self.rect=self.canvas.create_rectangle(x1,y1,x2,y2,fill="")
        else:
            self.rect_list=[]
            self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.rect_list
 
        
    def previousImage(self):
        # print(self.annotation_dict)
        self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.rect_list
        self.current_index=(self.current_index - 1) % len(self.images)
        self.img = cv2.imread(self.images[self.current_index])
        self.img = cv2.resize(self.img,(500,500))
        self.img_tk = Image.fromarray(self.img)
        self.image = itk.PhotoImage(image=self.img_tk)
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        if os.path.basename(self.images[self.current_index]) in self.annotation_dict.keys():
            # print(self.annotation_dict[os.path.basename(self.images[self.current_index])])
            # x=self.annotation_dict[os.path.basename(self.images[self.current_index])][0]
            # y=self.annotation_dict[os.path.basename(self.images[self.current_index])][1]
            # cv2.circle(self.img,(x,y),1,(255,0,0),3)
            self.rect_list=self.annotation_dict[os.path.basename(self.images[self.current_index])]
            for i in self.rect_list:
                self.rect=self.canvas.create_rectangle(i[0],i[1],i[2],i[3],fill="")
        else:
            self.rect_list=[]
            self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.rect_list

    def clearLastRect(self):
        if len(self.rect_list)>0:
            del self.rect_list[-1]
        self.img = cv2.imread(self.images[self.current_index])
        self.img = cv2.resize(self.img,(500,500))
        self.img_tk = Image.fromarray(self.img)
        self.image = itk.PhotoImage(image=self.img_tk)
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        if os.path.basename(self.images[self.current_index]) in self.annotation_dict.keys():
            # print(self.annotation_dict[os.path.basename(self.images[self.current_index])])
            # x=self.annotation_dict[os.path.basename(self.images[self.current_index])][0]
            # y=self.annotation_dict[os.path.basename(self.images[self.current_index])][1]
            # cv2.circle(self.img,(x,y),1,(255,0,0),3)
            self.rect_list=self.annotation_dict[os.path.basename(self.images[self.current_index])]
            for i in self.rect_list:
                self.rect=self.canvas.create_rectangle(i[0],i[1],i[2],i[3],fill="")
        else:
            self.rect_list=[]
            self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.rect_list              
    def clearAllRect(self):
        if len(self.rect_list)>0:
            self.rect_list=[]
        self.img = cv2.imread(self.images[self.current_index])
        self.img = cv2.resize(self.img,(500,500))
        self.img_tk = Image.fromarray(self.img)
        self.image = itk.PhotoImage(image=self.img_tk)
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.rect_list              

    def quit(self):
        self.parent.destroy()

    def drag_start(self, event):
        """Begining drag of an object"""
        # record the item and its location
        if event.x<500 and event.y<500:
            self.start=[event.x,event.y]
            self.rect=self.canvas.create_rectangle(self.start[0],self.start[1],self.start[0],self.start[1],fill="")
        # print(self.rect)
    def drag_stop(self, event):
        """End drag of an object"""
        if event.x<500 and event.y<500 and self.start!=[-1,-1]:
            self.rect_list.append([self.start[0],self.start[1],event.x,event.y])
            self.start=[-1,-1]

    def drag(self, event):
        """Handle dragging of an object"""
        if event.x<500 and event.y<500 and self.start!=[-1,-1]:
            self.canvas.coords(self.rect, self.start[0],self.start[1],event.x,event.y)



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
            # PointAnnotation(root_point,images_folder).pack(fill="both", expand=True)
            PointAnnotate(root_point,images_folder).pack(fill="both", expand=True)
            root_point.mainloop()
        if temp.point==2:
            images_folder='D:/Vijay Code/Personal Projects/Hockey_puck_track/dataset/images/1/'
            root_point = tk.Tk()
            root_point.title("Image Scanner")
            RectangleAnnotate(root_point,images_folder).pack(fill="both", expand=True)
            root_point.mainloop()

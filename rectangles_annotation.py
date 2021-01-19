import cv2
import imutils
from PIL import Image
from PIL import ImageTk as itk
import tkinter as tk
from tkinter import ttk
import glob
import os
import csv



class RectangleAnnotate(tk.Frame):
    """ Capture rectangles by means of mouse click and drag, navigate through the directory and save the final data as csv """

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

        # Create buttons and their functionality
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
        self.canvas.bind("<ButtonPress-1>", self.drag_start)
        self.canvas.bind("<ButtonRelease-1>", self.drag_stop)
        self.canvas.bind("<B1-Motion>", self.drag)


    def saveData(self):
        """ Save all the captured rectangles of all the images as a csv file under the appropriate headers """
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
        """ Go to the next image and display all the associated rectangles captured for it """

        self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.rect_list
        self.current_index=(self.current_index + 1) % len(self.images)
        self.img = cv2.imread(self.images[self.current_index])
        self.img = cv2.resize(self.img,(500,500))
        self.img_tk = Image.fromarray(self.img)
        self.image = itk.PhotoImage(image=self.img_tk)
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW) 
        if os.path.basename(self.images[self.current_index]) in self.annotation_dict.keys():
            self.rect_list=self.annotation_dict[os.path.basename(self.images[self.current_index])]
            for x1,y1,x2,y2 in self.rect_list:
                self.rect=self.canvas.create_rectangle(x1,y1,x2,y2,fill="")
        else:
            self.rect_list=[]
            self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.rect_list
 
        
    def previousImage(self):
        """ Go to the previous image and display all the associated rectangles captured for it """
        self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.rect_list
        self.current_index=(self.current_index - 1) % len(self.images)
        self.img = cv2.imread(self.images[self.current_index])
        self.img = cv2.resize(self.img,(500,500))
        self.img_tk = Image.fromarray(self.img)
        self.image = itk.PhotoImage(image=self.img_tk)
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        if os.path.basename(self.images[self.current_index]) in self.annotation_dict.keys():
            self.rect_list=self.annotation_dict[os.path.basename(self.images[self.current_index])]
            for i in self.rect_list:
                self.rect=self.canvas.create_rectangle(i[0],i[1],i[2],i[3],fill="")
        else:
            self.rect_list=[]
            self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.rect_list


    def clearLastRect(self):
        """ Clear the most recently captured rectangle for the given image """
        if len(self.rect_list)>0:
            del self.rect_list[-1]
        self.img = cv2.imread(self.images[self.current_index])
        self.img = cv2.resize(self.img,(500,500))
        self.img_tk = Image.fromarray(self.img)
        self.image = itk.PhotoImage(image=self.img_tk)
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        if os.path.basename(self.images[self.current_index]) in self.annotation_dict.keys():
            self.rect_list=self.annotation_dict[os.path.basename(self.images[self.current_index])]
            for i in self.rect_list:
                self.rect=self.canvas.create_rectangle(i[0],i[1],i[2],i[3],fill="")
        else:
            self.rect_list=[]
            self.annotation_dict[os.path.basename(self.images[self.current_index])]=self.rect_list  
            
    def clearAllRect(self):
        """ Clear all the captured rectangles for the given image """
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
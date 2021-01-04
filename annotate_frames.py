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

class Example(tk.Frame):
    """Illustrate how to drag items on a Tkinter canvas"""

    def __init__(self, parent,images_folder):
        tk.Frame.__init__(self, parent)

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

        self.canvas.create_window(self.img.shape[1],self.img.shape[0]/2-50,anchor=tk.SW,window=B_next)
        self.canvas.create_window(self.img.shape[1],self.img.shape[0]/2,anchor=tk.SW,window=B_back)
        self.canvas.create_window(self.img.shape[1],self.img.shape[0]/2+50,anchor=tk.SW,window=B_save)

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
        ok_button.place(x=90,y=70)
    def submit(self):
        self.root.destroy()
    def browse(self):
        # Tk().withdraw() 
        self.foldername = filedialog.askdirectory()
        self.folder.set(self.foldername)



if __name__ == "__main__":
    """
    root = tk.Tk()
    file = filedialog.askopenfile(parent=root,mode='rb',title='Choose a file')
    if file:
        data = file.read()
        file.close()
        print("I got %d bytes from this file." % len(data))
    """
    root1=tk.Tk()
    root1.geometry('250x125')
    temp=initialDialogue(root1)
    root1.mainloop()
    print(temp.foldername, temp.v0)
    image_name="dataset/images/1/"
    root = tk.Tk()
    root.title("Image Scanner")
    # root.geometry("4000x4000")
    Example(root,image_name).pack(fill="both", expand=True)
    root.mainloop()
# exit(0)











# def draw_circle(event,x,y,flags,param):
#     global mouseX,mouseY
#     if event == cv2.EVENT_LBUTTONDBLCLK:
#         cv2.circle(img,(x,y),2,(255,0,0),-1)
#         mouseX,mouseY = x,y

# img = cv2.imread('pages.jpg')
# print(img.shape)
# cv2.namedWindow('image')
# cv2.setMouseCallback('image',draw_circle)
# lists=[]
# while(1):
#     cv2.imshow('image',img)
#     k = cv2.waitKey(20) & 0xFF
#     if k == 27:
#         break
#     elif k == ord('a'):
#         print(mouseX,mouseY)
#         lists.append([mouseX,mouseY])
#     elif k==ord('q'):
#         cv2.destroyAllWindows()
#         break
# # exit(0)
# # img = cv2.imread('sudokusmall.png')

# rows,cols,ch = img.shape

# # pts1 = np.float32([[56,65],[368,52],[28,387],[389,390]])
# pts1=np.float32(lists)
# pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])
# print(pts1)
# M = cv2.getPerspectiveTransform(pts1,pts2)

# dst = cv2.warpPerspective(img,M,(300,300))

# plt.subplot(121),plt.imshow(img),plt.title('Input')
# plt.subplot(122),plt.imshow(dst),plt.title('Output')
# plt.show()

# warped = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
# # T = threshold_local(warped, 11, offset = 10, method = "gaussian")
# # print(T.shape)
# for i in range(50,150,10):
#     # warped = (warped > i).astype("uint8") * 255
#     ret, thresh2 = cv2.threshold(warped, i, 255, cv2.THRESH_BINARY_INV) 

#     # cv2.imshow("Scanned", imutils.resize(warped, height = 650))
#     cv2.imshow('scanned',thresh2)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
# exit(0)

# img = cv2.imread('drawing.png')
# rows,cols,ch = img.shape

# pts1 = np.float32([[50,50],[200,50],[50,200]])
# pts2 = np.float32([[10,100],[200,50],[100,250]])

# M = cv2.getAffineTransform(pts1,pts2)

# dst = cv2.warpAffine(img,M,(cols,rows))

# plt.subplot(121),plt.imshow(img),plt.title('Input')
# plt.subplot(122),plt.imshow(dst),plt.title('Output')
# plt.show()

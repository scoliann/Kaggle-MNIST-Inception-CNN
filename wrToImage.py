from tkinter import *
from PIL import Image, ImageDraw
import os

canvas_width = 500
canvas_height = 250
white = (255, 255, 255)

image1 = Image.new("RGB", (canvas_width, canvas_height), "black")
draw = ImageDraw.Draw(image1)
pointslist=[]

def paint( event ):
   python_green = "black"
   x1, y1 = ( event.x - 1 ), ( event.y - 1 )
   x2, y2 = ( event.x + 1 ), ( event.y + 1 )
   w.create_oval( x1, y1, x2, y2, fill = python_green, width=10)
   pointslist.append((x1, y1))

master = Tk()
master.title( "Handwriting recognition" )
w = Canvas(master, 
           width=canvas_width, 
           height=canvas_height)
w.pack(expand = YES, fill = BOTH)
w.bind( "<B1-Motion>", paint)


def generateImage():
    draw.line(pointslist, white, width=10)
    w.postscript(file="my_drawing.ps", colormode='color')
    filename = "my_drawing.jpg"
    image1.save(filename)
    exit()
    

frame = Frame(master, bg='grey', width=20, height=40)
frame.pack(fill='x')
button1=Button(frame, text='Make image', command=generateImage)
button1.pack(side='left', padx=10)



# PIL image can be saved as .png .jpg .gif or .bmp file (among others)

w.mainloop()

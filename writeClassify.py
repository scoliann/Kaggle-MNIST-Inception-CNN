from tkinter import *
from PIL import Image, ImageDraw
import os


#For INCEPTIONV3
import tensorflow as tf
from os import listdir
from os.path import isfile, join
#from natsort import natsorted
import pandas as pd

def printPrediction(lisimage, lenimage):
    for imageCounter in range(lenimage):
        print('On Image ' + str(imageCounter+1) + '/' + str(lenimage))
        print("prediction here", lisimage[imageCounter])

    
def pleaseClassify():
    # Read in photos for each class and encode
    testSetFolder = 'testSet2'
    testSetPhotos = [join(testSetFolder, f) for f in listdir(testSetFolder) if isfile(join(testSetFolder, f))]
    sortedTestSetPhotos = testSetPhotos #sorted(testSetPhotos)
    print("hersomeooooo",  testSetPhotos)
    encodedTestSetPhotos = [tf.gfile.FastGFile(photo, 'rb').read() for photo in sortedTestSetPhotos]
    X = encodedTestSetPhotos

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line in tf.gfile.GFile("newoutput_labels.txt")]

    # Unpersists graph from file
    with tf.gfile.FastGFile("newoutput_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    # Make predictions
    predictionList = []
    with tf.Session() as sess:

        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        # Iterate over all images and make predictions
        imageCounter = 0
        for image_data in X:

            # Print image coutner to terminal
            imageCounter += 1

            # Make a prediction
            predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

            # Get the predicted class and add it to list of predictions
            prediction = label_lines[top_k[0]]
            predictionList.append(prediction)
    printPrediction(predictionList, len(X))

    # Create Submission CSV file
    results = pd.DataFrame({'ImageId': pd.Series(range(1, len(predictionList) + 1)), 'Label': pd.Series(predictionList)})
    results.to_csv('results.csv', index=False)


def calculateAccuracy():
    ans=int(input("How many did I get wrong: "))
    print("Accuracy is ", str(((10-ans)/10)*100)+ " percent")
    print("Thanks for your feedback")


def multipleCanvas(num):
    canvas_width = 250
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
    master.title( "Num:"+str(num+1) )
    w = Canvas(master, 
               width=canvas_width, 
               height=canvas_height)
    w.pack(expand = YES, fill = BOTH)
    w.bind( "<B1-Motion>", paint)


    def generateImage():
        image1.resize((28,28), Image.ANTIALIAS)
        draw.line(pointslist, white, width=25)
        w.postscript(file="my_drawing.ps", colormode='color')
        filename="testSet2/"+str(num)+".jpg"
        image1.save(filename)
        foo=Image.open(filename)
        foo=foo.resize((28,28),Image.ANTIALIAS)
        foo.save(filename, quality=95)
        if num==9:
            pleaseClassify()
            calculateAccuracy()
            exit()
        multipleCanvas(num+1)
    

    frame = Frame(master, bg='grey', width=250, height=250)
    frame.pack(fill='x')
    button1=Button(frame, text='Make image', command=generateImage)
    button1.pack(side='left', padx=10)

    w.mainloop()

multipleCanvas(0)


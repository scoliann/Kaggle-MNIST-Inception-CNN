'''
This file has been adopted and modified from the label_image.py base code provided on the TensorFlow for Poets tutorial on Codelabs. 
	Link:  https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/index.html?index=..%2F..%2Findex#0
'''

import tensorflow as tf
from os import listdir
from os.path import isfile, join
#from natsort import natsorted
import pandas as pd

# Read in photos for each class and encode
testSetFolder = 'testSet'
testSetPhotos = [join(testSetFolder, f) for f in listdir(testSetFolder) if isfile(join(testSetFolder, f))]
sortedTestSetPhotos = sorted(testSetPhotos)
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
		print('On Image ' + str(imageCounter) + '/' + str(len(X)))

		# Make a prediction
		predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
		# Sort to show labels of first prediction in order of confidence
		top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

		# Get the predicted class and add it to list of predictions
		prediction = label_lines[top_k[0]]
		print("prediction here", prediction)
		predictionList.append(prediction)

# Create Submission CSV file
results = pd.DataFrame({'ImageId': pd.Series(range(1, len(predictionList) + 1)), 'Label': pd.Series(predictionList)})
results.to_csv('results.csv', index=False)






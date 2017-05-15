'''
The purpose of this script is to read in the train.csv and test.csv files provided by Kaggle, and convert the lines of text into .jpg images.
Essentially, I am just changing the form of the training and test set.
This is done so that the .jpg images can be used to retrain TensorFlow's Inception-v3 model.
'''

import pandas as pd
from PIL import Image
import numpy as np
import os

trainingSetDir = 'trainingSet'
testSetDir = 'testSet'

# Create training set and test set folders if they do not exist
if not os.path.isdir(trainingSetDir):
	os.makedirs(trainingSetDir)
if not os.path.isdir(testSetDir):
	os.makedirs(testSetDir)

# Read in training data from train.csv
dfTrain = pd.read_csv('train.csv')
trainLabelsList = dfTrain['label'].tolist()
dfTrainFeatureVectors = dfTrain.drop(['label'], axis=1)
trainFeatureVectors = [fv.reshape(28, 28) for fv in dfTrainFeatureVectors.values.astype(dtype=np.uint8)]

# Read in test data from test.csv
dfTest = pd.read_csv('test.csv')
testFeatureVectors = [fv.reshape(28, 28) for fv in dfTest.values.astype(dtype=np.uint8)]

# Save images in training set as .jpg
for index in range(len(trainLabelsList)):

	# Print progress to terminal
	print('Training Set \t' + str(index + 1) + '/' + str(len(trainLabelsList)))

	# Get variables by index
	label = str(trainLabelsList[index])
	featureVector = trainFeatureVectors[index]

	# If folder does not exist for the class, then create it
	if not os.path.isdir(trainingSetDir + '/' + label):
		os.makedirs(trainingSetDir + '/' + label)

	# Save image to folder
	im = Image.fromarray(featureVector)
	im.save(trainingSetDir + '/' + label + '/' + 'img_' + str(index) + '.jpg')

# Save images in test set as .jpg
for index in range(len(testFeatureVectors)):

	# Print progress to terminal
	print('Test Set \t' + str(index + 1) + '/' + str(len(testFeatureVectors)))

	# Get variables by index
	featureVector = testFeatureVectors[index]
	imageId = str(index + 1)

	# Save image to folder
	im = Image.fromarray(featureVector)
	im.save(testSetDir + '/' + 'img_' + imageId + '.jpg')



























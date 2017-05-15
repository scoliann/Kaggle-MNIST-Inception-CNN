This script uses a retrained version of TensorFlow's Inception-v3 CNN to classify the Kaggle MNIST dataset. The results are then compared to those from a handmade CNN model.

## Inspiration

Since learning about TensorFlow's Inception-v3 model, I have been excited to compare its performance at classification tasks to models made from scratch.  Testing Inception-v3's performance on the MNIST dataset is a logical choice as my [CNN for Digit Recognition](https://github.com/scoliann/CNN-for-Digit-Recognition) project provides a baseline of the classification accuracies attainable by hand made models.

## About Inception and Transfer Learning 
 
The Inception-v3 model is a CNN built by Google to compete in the ImageNet competition.  Inception-v3 is therefore natively trained to classify input images into one of 1,000 categories used in ImageNet.  Transfer Learning is a method by which one retrains part of a pre-existing machine learning model for a new purpose.  In this case, we will be retraining the bottleneck layer of Inception-v3. The "bottleneck" layer is the neural network layer before the final softmax layer in the CNN.  Only one layer of the Inception-v3 model needs to be retrained, as the previous layers have already learned useful, generalizable functions such as edge detection. 

## About the Kaggle MNIST Dataset

Inception-v3 is retrained using a version of the MNIST dataset supplied in the [Kaggle Digit Recognizer](https://www.kaggle.com/c/digit-recognizer) competition.  The training set was used to retrain Inception-v3, and the test set was used to generate a submission file for the competition.  Retraining Inception-v3 requires .jpg files as input data.  Therefore, because the images in Kaggle's MNIST dataset are originally expressed as strings of pixel values, it was first necessary to convert the entire dataset (both training and test) to .jpg images.  This was done by running the `testToImages.py` script.

## Running the Scripts

To generate a submission file for the Kaggle Digit Recognizer competition, do the following:

1.  Use `python testToImages.py` to create the .jpg version of the Kaggle MNIST dataset.  The .jpg datasets will be saved in the `testSet` and `trainingSet` folders.
2.  Use `python classifier.py` to generate a `results.csv` file containing predictions for the Kaggle competition.

## Performance

After experimenting with a number of hyperparameter settings for retraining Inception-v3, I eventually reached a model that achieved 95.314% accuracy on the Kaggle Digit Recognizer test set.  This is significantly lower than the 98.357% accuracy achieved by my hand made [CNN for Digit Recognition](https://github.com/scoliann/CNN-for-Digit-Recognition) model.

## Thoughts / Lessons

1.  Retraining Inception-v3 is possible with a much smaller training set than training an entire CNN from scratch.  This is because only the final layer of the Inception-v3 model is retrained.
    - I retrained Inception-v3 with the entire 42,000 image training set provided by Kaggle.  This was probably a mistake, as it made the process take most of a day.  Obviously this is bad as it makes it difficult to try different hyperparameter combinations.
2.  Hyperparameter configurations that I did not have time to thoroughly test (eg. a smaller learning rate, etc.) may have resulted in better classification accuracy for the Inception-v3 model.
3.  Retraining Inception-v3 is done with the `retrain.py` file in TensorFlow.  This file does not include dropout or learning rate decay.  Modifying the `retrain.py` file to include these additions (and/or others) would likely improve the classification accuracy.

## Files

A brief description of files unmentioned till this point:

1.  `results.csv` is the Kaggle submission file made by the Inception model.
2.  `retrained_graph.pb` and `retrained_labels.txt` are used to read in the saved Inception model when making predictions.
3.  `sample_submission.csv` is an example submission file provided by Kaggle for this competition.
4.  `train.csv` is the CSV file of training data provided on Kaggle for the Digit Recognizer competition.
5.  `test.csv` is the CSV file of test data provided on Kaggle for the Digit Recognizer competition.

## Resources

A valuable resource for learning to retrain TensorFlow's Inception model is [TensorFlow for Poets](https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/index.html?index=..%2F..%2Findex#0).



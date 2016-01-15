
# -*- encoding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import precision_score
from sklearn.metrics import precision_recall_curve


from random import shuffle
import sys
import os

class Senti:

    def __init__(self):
        self.length = 0
        self.datafiles = ["positive_sentences", "negative_sentences"]
        self.sentiment = [0, 1]
#        self.sentiment = ["positive", "negative"]

#        self.ntraining = 100
        

            
        self.reviews = []
        self.categories = []
#        self.cat = []

        for f in range(len(self.datafiles)):            
            c = self.makecategorylist(self.datafiles[f], f)
            print len(c)
            self.categories += c
#            self.cat.append(f)
        print "c for loop end"
        print "categories: " , len(self.categories)

        self.reviews = map(self.readfile, self.datafiles) # read reviews
        
        self.t = []

        for f in range(len(self.reviews)):
            self.t = self.addarrays(self.t, self.reviews[f])

        self.text_clf = Pipeline([('vect', CountVectorizer()),
                             ('tfidf', TfidfTransformer()),
                             ('clf', SGDClassifier(loss = 'hinge',
                                                   penalty = 'l2',
                                                   alpha=1e-3, n_iter=5,
                                                   random_state = 30))
                             ])


        print "categories: " , len(self.categories)

        self.createtrainingandtestfiles(self.datafiles)
        self.trainmodel()
        self.testmodel()

#        _ = self.text_clf.fit(self.t, self.categories) #training the classifier
                    
    def readfile(self, filename):
        f = open(filename, 'r')
        content = f.readlines()
        return content

    def addarrays(self, s, t):
        return s + t

    def makecategorylist(self, filename, a):
        content = self.readfile(filename)
        categories = [a] * len(content)
        return categories

    def predictsentiment(self, sentence):
        prediction = self.text_clf.predict([sentence])
        return self.sentiment[prediction]

    def writestringtofile(self, filename, string):
        f = open(filename, 'a')
#        print string
        f.write(string)
        f.close()
        
    def createtrainingandtestfiles(self, datafiles):

        print "createtrainingandtestfiles"
        r = map(self.readfile, datafiles) # arrays which have contents of files
        reviews = []

        for f in range(len(r)): # contents into one array
            reviews += r[f]

        categories = []
        for f in range(len(datafiles)):
            c = self.makecategorylist(datafiles[f], f)
            categories += c

        ntraining = 250
        ntest = len(reviews) - ntraining

        revcat = []
        for f in range(len(reviews)):
            revcat.append([reviews[f], categories[f]])

        print len(revcat)

        shuffle(revcat)
        shuffle(revcat)
        shuffle(revcat)
                    
        trainingset = revcat[0:ntraining]
        testingset = revcat[ntraining:]

        print "sets"

        print trainingset[0]
        print trainingset[0][1]
        print len(trainingset)
        print len(testingset)

        positive_reviews_training_file = "positive_reviews_training"
        negative_reviews_training_file = "negative_reviews_training"

        if os.path.exists(positive_reviews_training_file):
            os.remove(positive_reviews_training_file)

        if os.path.exists(negative_reviews_training_file):
            os.remove(negative_reviews_training_file)        
        

        for f in range(len(trainingset)):

#        for f in range(1,3):

            if(trainingset[f][1] == 0):
                self.writestringtofile(positive_reviews_training_file, trainingset[f][0])
            if(trainingset[f][1] == 1):
                self.writestringtofile(negative_reviews_training_file, trainingset[f][0])
        test_reviews_file = "test_reviews"
        test_categories_file = "test_categories"
        if os.path.exists(test_reviews_file):
            os.remove(test_reviews_file)
        if os.path.exists(test_categories_file):
            os.remove(test_categories_file)
                
        for f in range(len(testingset)):
            self.writestringtofile(test_reviews_file, testingset[f][0])
            self.writestringtofile(test_categories_file, str(testingset[f][1]) + "\n")


    def trainmodel(self):
        reviews = []
        categories = []
        trainingfiles = ["positive_reviews_training", "negative_reviews_training"]
        r = map(self.readfile, trainingfiles)
        for f in range(len(r)):
            reviews += r[f]

        for f in range(len(trainingfiles)):
            categories += self.makecategorylist(trainingfiles[f], f)

        print "trainmodel"
        print len(reviews)
        print len(categories)
            
        _ = self.text_clf.fit(reviews, categories)

    def testmodel(self):
        reviews = self.readfile("test_reviews")
        categories = self.readfile("test_categories")
        results = []

        print "testmodel"
        print len(reviews)
        print len(categories)

        for f in range(len(reviews)):
            results.append(int(self.predictsentiment(reviews[f])))

        categories = [int(i) for i in categories]

        if(isinstance(categories[0], int)):
           print "categories int"

        c = self.countconfusionmatrix(categories, results)
        d = precision_recall_fscore_support(categories, results)
        print "precision"
        print d[0]
        print "recall"
        print d[1]
        print "fscore"
        print d[2]
        print "support"
        print d[3]

        e = precision_score(categories, results)
        f = precision_recall_curve(categories, results)
        
    
    def countaccuracy(self, tp, tn, fp, fn):
        a = (tp + tn) / (tp + tn + fp + fn)
        return a

    def countconfusionmatrix(self, actual, results):
        c = confusion_matrix(actual, results)
        print c
        return c

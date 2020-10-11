# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 10:46:28 2020

@author: Abheeshta
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from imblearn.over_sampling import RandomOverSampler, SMOTE
from sklearn.model_selection import train_test_split
from sklearn import model_selection, preprocessing, svm, metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import recall_score, accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pickle
import joblib


amazon_DF = pd.read_csv("Induction_Data_New.csv")
amazon_DF.dropna(axis = 0, inplace = True)
amazon_DF_clean = amazon_DF.copy()
stop_words = stopwords.words("english")



##########----- CLEANING THE DATA -----##########

def clean(s):
    s = s.lower()                   #Converting to lower case
    s = re.sub(r'[^\w\s]', ' ', s)  #Removing punctuation
    s = re.sub(r'[\d+]', ' ', s)    #Removing Numbers
    s = s.strip()                   #Removing trailing spaces
    s = re.sub(' +', ' ', s)        #Removing extra whitespaces
    return s

# Removal of punctuation, digits and extra spaces
amazon_DF_clean["Reviews"] = amazon_DF_clean["Reviews"].apply(lambda x: clean(x))

# Remove stop words
amazon_DF_clean["Reviews"] = amazon_DF_clean["Reviews"].apply(lambda x: " ".join(x for x in x.split() if x not in stop_words))

#Sentiment Analysis
senti = SentimentIntensityAnalyzer()
amazon_DF_clean["Sentiment_VADER"] = amazon_DF_clean["Reviews"].apply(lambda x: senti.polarity_scores(x)['compound'])

def sentiment_result(polarity):
    if polarity >= 0.1:
        return "Positive"
    elif polarity <= -0.1:
        return "Negative"
    else:
        return "Neutral"

amazon_DF_clean["Label"] = amazon_DF_clean["Sentiment_VADER"].apply(lambda x: sentiment_result(x))

##########----- MODEL BUILDING -----##########

# Count Vectorizer
count_vect = CountVectorizer(max_features=5000)
X = count_vect.fit_transform(amazon_DF_clean["Reviews"]).toarray()


# Train and Test Split
X_train, X_test, y_train, y_test = train_test_split(X, amazon_DF_clean["Label"], test_size = 0.1, random_state = 42)

# Oversampling
oversample = SMOTE(random_state = 42, sampling_strategy = 'minority')
X_train_oversample, y_train_oversample = oversample.fit_sample(X_train, y_train)


# MODEL = Linear Support Vector Classifier (OvR)


svc = svm.LinearSVC(multi_class = 'ovr')
svc.fit(X_train_oversample, y_train_oversample)
svc_pred = svc.predict(X_test)

# MODEL SAVED TO ANOTHER FILE
joblib.dump(svc, 'final_model.pkl')
joblib.dump(count_vect, 'vector.pkl')



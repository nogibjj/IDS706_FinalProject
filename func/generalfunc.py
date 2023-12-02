import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import matplotlib.pyplot as plt
from string import punctuation
from nltk.corpus import stopwords, wordnet
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize,sent_tokenize
from wordcloud import WordCloud
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression,SGDClassifier, LinearRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from keras.layers import Dense, Conv1D, MaxPool1D, Flatten, Dropout
from keras.models import Sequential
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score,confusion_matrix
import missingno as miss
import joblib
from keras.models import load_model
def loadVectorizer(vectorizer_path):
    loaded_count_vec = joblib.load(vectorizer_path) 
    return loaded_count_vec

def preprocessNewdata(raw_string, loaded_count_vec):
    new_data = pd.Series(raw_string)
    new_data_vec = loaded_count_vec.transform(new_data).todense()
    return new_data_vec

def loadModel(save_path):
    loaded_model= load_model(save_path)
    return loaded_model


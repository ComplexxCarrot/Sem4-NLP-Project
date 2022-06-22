# main import
import numpy as np
import pandas as pd

# machine learning stuff
import re
import sqlite3
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import LogisticRegression
from sqlite3 import Error
from sklearn.ensemble import RandomForestClassifier
nltk.download('stopwords')
%matplotlib inline

# using TF-IDF text classification
count_vect = CountVectorizer()

def run_ML():
	url = 'https://gist.githubusercontent.com/agtbaskara/a1a7017027cc1df9d35cf06e1e5575b7/raw/59870e27ca217d77ac0d8d8dc100551c0dcd14b3/dataset_sms_spam_v2.csv'
	dataset = pd.read_csv(url, encoding= 'utf-8')
	dataset['label'] = dataset['label'].replace(['promo','penipuan'],['spam','spam'])

	nltk.download('stopwords')
	stemmer = PorterStemmer()
	words = stopwords.words("english")
	dataset['cleaned'] = dataset['Teks'].apply(lambda x: " ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower())

	vectorizer = TfidfVectorizer(min_df= 3, stop_words="english", sublinear_tf=True, norm='l2', ngram_range=(1, 2))
	final_features = vectorizer.fit_transform(dataset['cleaned']).toarray()

	X = dataset['cleaned']
	Y = dataset['label']
	X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25)

	pipeline = Pipeline([('vect', vectorizer),
                     ('chi',  SelectKBest(chi2, k=1200)),
                     ('clf', LogisticRegression(random_state=0))])

	model = pipeline.fit(X_train, y_train)
	with open('LogisticRegression.pickle', 'wb') as f:
    		pickle.dump(model, f)
	
	return model

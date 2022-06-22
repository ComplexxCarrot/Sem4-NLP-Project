# main import
import numpy as np
import pandas as pd

# machine learning stuff
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import LogisticRegression
nltk.download('stopwords')

def run_ML():
	url = 'https://raw.githubusercontent.com/ComplexxCarrot/Sem4-NLP-Project/main/spam-datasets.csv'
	dataset = pd.read_csv(url, encoding= 'iso-8859-1')
	

	nltk.download('stopwords')
	stemmer = PorterStemmer()
	words = stopwords.words("english")
	dataset['cleaned'] = dataset['v2'].apply(lambda x: " ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower())

	vectorizer = TfidfVectorizer(min_df= 3, stop_words="english", sublinear_tf=True, norm='l2', ngram_range=(1, 2))
	final_features = vectorizer.fit_transform(dataset['cleaned']).toarray()

	X = dataset['cleaned']
	Y = dataset['v1']

	pipeline = Pipeline([('vect', vectorizer),
                     ('chi',  SelectKBest(chi2, k=1200)),
                     ('clf', LogisticRegression(random_state=0))])

	model = pipeline.fit(X, Y)
	
	return model

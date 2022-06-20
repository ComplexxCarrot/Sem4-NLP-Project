# main import
import pandas as pd

# machine learning stuff
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

# using TF-IDF text classification
count_vect = CountVectorizer()

def run_ML():
	url = 'https://gist.githubusercontent.com/agtbaskara/a1a7017027cc1df9d35cf06e1e5575b7/raw/59870e27ca217d77ac0d8d8dc100551c0dcd14b3/dataset_sms_spam_v2.csv'
	df = pd.read_csv(url, encoding= 'utf-8')
	# df['label'] = df['label'].replace(['promo','penipuan'],['spam','spam'])
	df = pd.read_csv(url, encoding= 'iso-8859-1')
	X_train = df['Teks']
	y_train = df['label']

	X_train_counts = count_vect.fit_transform(X_train)
	tfidf_transformer = TfidfTransformer()
	X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
	clf = MultinomialNB().fit(X_train_tfidf, y_train)
	return clf

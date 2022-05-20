# main import
import pandas as pd

# machine learning stuff
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

# using TF-IDF text classification

count_vect = CountVectorizer()

def run_ML():
  print('Machine starts learning...')
  
  url = 'https://raw.githubusercontent.com/ComplexxCarrot/Sem4-NLP-Project/main/spam-datasets.csv'
  df = pd.read_csv(url, encoding= 'iso-8859-1')
  df = df[['v1','v2']]
  print('data taken...')
  
  # remove nan (not available) values
  df.dropna(subset = ["v2"], inplace=True)

  print('nan values removed...')

  X_train = df['v2']
  y_train = df['v1']

  print('training data runs...')
  
  X_train_counts = count_vect.fit_transform(X_train)

  print('count vectorizer done...')
  
  tfidf_transformer = TfidfTransformer()
  X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

  print('transform to tfidf done...')
  
  clf = MultinomialNB().fit(X_train_tfidf, y_train)

  print('machine done learning, saving training results...')
  
  return clf
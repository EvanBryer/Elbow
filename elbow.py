import argparse
parser = argparse.ArgumentParser(description='Perform Sillhouette analysis for k-means clustering.')
req = parser.add_argument_group('Required arguments')
req.add_argument("-p", "--path", help="path to file of new line delimited strings.", required=True)
req.add_argument("-s", "--start", help="Starting number of clusters. Must be > 1.", type=int, required=True)
req.add_argument("-e","--end", help="Ending number of clusters. Must be < len(strings).", type=int, required=True)
parser.add_argument("--step", help="Step size for looping from start to end. Defualt is 10.", type=int, default=10)
req = parser.parse_args()
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt

#Cleaning the text
import string
def text_process(text):
    '''
    Takes in a string of text, then performs the following:
    1. Remove all punctuation
    2. Remove digits
    3. Remove all stopwords from included languages
   	4. Return the cleaned text as a list of words
    '''
    stemmer = WordNetLemmatizer()
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join([i for i in nopunc if not i.isdigit()])
    nopunc =  [word.lower() for word in nopunc.split() if word not in stopwords.words('english') and word not in stopwords.words('french') and word not in stopwords.words('german') 			and word not in stopwords.words('spanish') and word not in stopwords.words('italian') and word not in stopwords.words('dutch')]
    return [stemmer.lemmatize(word) for word in nopunc]

print("Start")
from sklearn.feature_extraction.text import TfidfVectorizer

X_train = open(req.path).readlines()

tfidfconvert = TfidfVectorizer(analyzer=text_process,ngram_range=(1,3)).fit(X_train)
print("Converted")
x=tfidfconvert.transform(X_train)
print("Transformed")

Sum_of_squared_distances = []
kmax = req.end
r = range(req.start, kmax+1, req.step)

for k in r:
    km = KMeans(n_clusters=k)
    km = km.fit(x)
    Sum_of_squared_distances.append(km.inertia_)


import matplotlib.pyplot as plt

plt.plot(r, Sum_of_squared_distances, 'bx-')
plt.xlabel('k')
plt.ylabel('Sum_of_squared_distances')
plt.title('Elbow Method For Optimal k')
plt.show()

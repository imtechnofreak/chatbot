import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.metrics.pairwise import cosine_similarity

class TFIDFPredictor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix_train = None

    def train(self, data):
        self.vectorizer.fit(data.message.values)
        self.train_data = data
        self.tfidf_matrix_train = self.vectorizer.transform(data.message.values) 
        
    def predict(self, context):
        # Convert context and utterances into tfidf vector
        vector_context = self.vectorizer.transform([context])
        #vector_doc = self.vectorizer.transform(utterances)
        vector_doc = self.tfidf_matrix_train
        
        # The dot product measures the similarity of the resulting vectors
        #result = np.dot(vector_doc, vector_context.T).todense()
        #result = np.asarray(result).flatten()
        result = cosine_similarity(vector_doc, vector_context)
        result = np.asarray(result).flatten()
        
        # Sort by top results and return the indices in descending order
        return np.argsort(result, axis=0)[::-1][:5], np.sort(result, axis=0)[::-1][:5]

'''
train_data = pd.read_csv('../data/conversations.csv')
tfidf = TFIDFPredictor()
tfidf.train(train_data)
'''

def main():
    import os
    import pickle

    '''
    pkl_file_path = os.path.join(os.path.curdir, 'tfidf_predictor.pickle')
    with open(pkl_file_path, 'wb') as f:
        pickle.dump(tfidf, f)
    '''

    pkl_file_path = os.path.join(os.path.curdir, 'tfidf_predictor.pickle')
    with open(pkl_file_path, 'rb') as f:
        tfidf = pickle.load(f)


    train_data = tfidf.train_data

    while True:
        user_message = input("Enter message: \t")
        y_pred, y_values = tfidf.predict(user_message)
        for idx, (pred, val) in enumerate(zip(y_pred, y_values)):
            print("(%d) %s => %s [%.4f]" % (idx, train_data.iloc[pred].message, train_data.iloc[pred].response , val))


if __name__ == '__main__':
    main()

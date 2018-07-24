import numpy as np
import pandas as pd
import pickle
import io
import os
import warnings

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity

from rasa_core.policies.policy import Policy
from rasa_core.actions.action import ACTION_LISTEN_NAME

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


class TfidfPolicy(Policy):
    def __init__(self, featurizer=None, max_history=None, tfidf=None):
        super(TfidfPolicy, self).__init__(featurizer, max_history)
        self.tfidf = tfidf

    def persist(self, path):
        if self.tfidf:
            pkl_file_path = os.path.join(path, 'tfidf_predictor.pickle')
            with open(pkl_file_path, 'wb') as f:
                pickle.dump(self.tfidf, f)
        else:
            warnings.warn("Persist called without a trained model present. "
                          "Nothing to persist then!")


    def train(self, X, domain, **kwargs):
        # type: (ndarray, List[int], Domain, **Any) -> None
        """Trains the policy on given training data."""
        self.train_data = pd.read_csv("./data/conversations.csv")
        self.tfidf = TFIDFPredictor()
        self.tfidf.train(self.train_data)

    def predict_action_probabilities(self, tracker, domain):
        if tracker.latest_action_name == ACTION_LISTEN_NAME:
            txt = tracker.latest_message.text
            y_pred, y_values = self.tfidf.predict(txt)
            for idx, (pred, val) in enumerate(zip(y_pred, y_values)):
                print("\t(%d) %s => %s [%.4f]" % (idx, self.tfidf.train_data.iloc[pred].message, 
                                            self.tfidf.train_data.iloc[pred].response , val))        

            return np.zeros(domain.num_actions)
        else:
            return np.zeros(domain.num_actions)

    @classmethod
    def load(cls, path, featurizer, max_history):
        if os.path.exists(path):
            meta_path = os.path.join(path, "tfidf_predictor.pickle")
            if os.path.isfile(meta_path):
                with io.open(meta_path, "rb") as f:
                    tfidf = pickle.load(f)
                return cls(max_history=max_history,
                           featurizer=featurizer, tfidf=tfidf)
            else:
                print("Creating new class")
                return cls(max_history=max_history,
                           featurizer=featurizer)
        else:
            raise Exception("Failed to load dialogue model. Path {} "
                            "doesn't exist".format(os.path.abspath(path)))
    
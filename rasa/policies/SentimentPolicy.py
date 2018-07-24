import numpy as np
import pandas as pd
import pickle
import io
import os
import warnings
from textblob import TextBlob

from rasa_core.policies.policy import Policy
from rasa_core.actions.action import ACTION_LISTEN_NAME


class SentimentPolicy(Policy):
    def __init__(self, featurizer=None, max_history=None):
        super(SentimentPolicy, self).__init__(featurizer, max_history)

    def persist(self, path):
        pass
        warnings.warn("Persist called without a trained model present. "
                        "Nothing to persist then!")


    def train(self, X, domain, **kwargs):
        # type: (ndarray, List[int], Domain, **Any) -> None
        """Trains the policy on given training data."""
        pass

    def predict_action_probabilities(self, tracker, domain):
        if tracker.latest_action_name == ACTION_LISTEN_NAME:
            txt = tracker.latest_message.text
            print(tracker.latest_message)
            blobs = TextBlob(txt)
            polarity = np.mean([sentence.sentiment.polarity for sentence in blobs.sentences])
            print("%s [%.3f]" % (txt, polarity))

            return np.zeros(domain.num_actions)
        else:
            return np.zeros(domain.num_actions)

    @classmethod
    def load(cls, path, featurizer, max_history):
        if os.path.exists(path):
            print("Creating new class")
            return cls(max_history=max_history,
                        featurizer=featurizer)
        else:
            raise Exception("Failed to load dialogue model. Path {} "
                            "doesn't exist".format(os.path.abspath(path)))
    
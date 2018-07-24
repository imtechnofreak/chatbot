import numpy as np
import pandas as pd
import string
import re
import random
import os
import json
import logging


from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.policy import Policy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.policies.ensemble import PolicyEnsemble
from rasa_core.actions.action import ACTION_LISTEN_NAME
from rasa_core import utils

from policies.ElizaPolicy import *
from policies.TfidfPolicy import *
from policies.SentimentPolicy import *

logger = logging.getLogger(__name__)


class CustomPolicy(KerasPolicy):
    def model_architecture(self, num_features, num_actions, max_history_len):
        """Build a Keras model and return a compiled model."""
        from keras.layers import LSTM, Activation, Masking, Dense
        from keras.models import Sequential

        n_hidden = 32  # size of hidden layer in LSTM
        # Build Model
        batch_shape = (None, max_history_len, num_features)

        model = Sequential()
        model.add(Masking(-1, batch_input_shape=batch_shape))
        model.add(LSTM(n_hidden, batch_input_shape=batch_shape))
        model.add(Dense(input_dim=n_hidden, output_dim=num_actions))
        model.add(Activation('softmax'))

        model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])

        logger.debug(model.summary())
        return model

class NewPolicyEnsemble(PolicyEnsemble):
    def __init__(self, policies, known_slot_events=None):
        super(NewPolicyEnsemble, self).__init__(policies, known_slot_events)

    def probabilities_using_best_policy(self, tracker, domain):
        result = None
        max_confidence = -1
        pname = None
        for p in self.policies:
            probabilities = p.predict_action_probabilities(tracker, domain)
            confidence = np.max(probabilities)
            pname = p.__class__.__name__
            max_index = np.argmax(probabilities)
            action_name = domain.action_for_index(max_index).name()
            logger.info("{} ({}) [{}]".format(action_name, confidence, pname))
            if confidence > max_confidence:
                max_confidence = confidence
                result = probabilities
        return result
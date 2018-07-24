import numpy as np
import random
import re

from rasa_core.policies.policy import Policy
from rasa_core.actions.action import ACTION_LISTEN_NAME

#----------------------------------------------------------------------
# gReflections, a translation table used to convert things you say
#    into things the computer says back, e.g. "I am" --> "you are"
#----------------------------------------------------------------------
gReflections = {
"am"   : "are",
"was"  : "were",
"i"    : "you",
"i'd"  : "you would",
"i've"  : "you have",
"i'll"  : "you will",
"my"  : "your",
"are"  : "am",
"you've": "I have",
"you'll": "I will",
"your"  : "my",
"yours"  : "mine",
"you"  : "me",
"me"  : "you"
}

#----------------------------------------------------------------------
# gPats, the main response table.  Each element of the list is a
#  two-element list; the first is a regexp, and the second is a
#  list of possible responses, with group-macros labelled as
#  %1, %2, etc.
#----------------------------------------------------------------------
gPats = [
[r'(.*) (suicide|kill myself)(.*)',
[ "I'm really sorry to hear that. I think you should get some help. Try visiting www.mentalhealthhelpline.ca/",
  "Please be careful. Try seeking help here: https://suicidepreention.ca/need-help/", 
  "I'm getting worried. You should try contacting someone at 1-866-925-5454 or good2talk.ca"]],

[r'quit',
[  "Thank you for talking with me.",
    "Good-bye.",
    "Thank you, that will be $150.  Have a good day!"]]
]

class ElizaPolicy(Policy): 
    def __init__(self, featurizer=None, max_history=None): 
        self.keys = list(map(lambda x:re.compile(x[0], re.IGNORECASE),gPats))
        self.values = list(map(lambda x:x[1],gPats))
        super(ElizaPolicy, self).__init__(featurizer, max_history)

    def predict_action_probabilities(self, tracker, domain):
        if tracker.latest_action_name == ACTION_LISTEN_NAME:
            txt = tracker.latest_message.text
            response = self.respond(txt)

            return np.zeros(domain.num_actions)
        else:
            return np.zeros(domain.num_actions)

    def train(self, X, domain, **kwargs):
        # type: (ndarray, List[int], Domain, **Any) -> None
        """Trains the policy on given training data."""
        pass

    #----------------------------------------------------------------------
    # translate: take a string, replace any words found in dict.keys()
    #  with the corresponding dict.values()
    #----------------------------------------------------------------------
    def translate(self, str, dict):
        words = str.lower().split()
        keys = dict.keys();
        for i in range(0,len(words)):
            if words[i] in keys:
                words[i] = dict[words[i]]
        return ' '.join(words)

    #----------------------------------------------------------------------
    #  respond: take a string, a set of regexps, and a corresponding
    #    set of response lists; find a match, and return a randomly
    #    chosen response from the corresponding list.
    #----------------------------------------------------------------------
    def respond(self, str):
        # find a match among keys
        for i in range(0, len(self.keys)):
            match = self.keys[i].match(str)
            if match:
                # found a match ... stuff with corresponding value
                # chosen randomly from among the available options
                resp = random.choice(self.values[i])
                # we've got a response... stuff in reflected text where indicated
                pos = resp.find('%')
                while pos > -1:
                    num = int(resp[pos+1:pos+2])
                    resp = resp[:pos] + \
                        self.translate(match.group(num),gReflections) + \
                        resp[pos+2:]
                    pos = resp.find('%')
                # fix munged punctuation at the end
                if resp[-2:] == '?.': resp = resp[:-2] + '.'
                if resp[-2:] == '??': resp = resp[:-2] + '?'
                return resp
        return ''

    @classmethod
    def load(cls, path, featurizer, max_history):
        return cls()
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import sys

from flask import request
from flask import make_response
from flask import Flask

import logging
import intents.weather as weather_handler
import intents.aimlbot as aiml_handler
import intents.greeting as greeting_handler

from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()

app = Flask(__name__)
logging.getLogger().setLevel(logging.INFO)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    # An action is a string used to identify what needs to be done in fulfillment
    action = req.get("result").get("action")

    # Parameters are any entites that Dialogflow has extracted from the request.
    parameters = req.get("result").get("parameters")

    # Contexts are objects used to track and store conversation state
    contexts = req.get("result").get("contexts")

    # Text coming from the user input
    query = req.get("result").get("resolvedQuery")
    score = req.get("result").get("score")

    logging.info("USER QUERY [score %.2f] : %s" % (score, query))

    ss = sid.polarity_scores(query)
    for k in sorted(ss):
        print('{0}: {1}, '.format(k, ss[k]), end='')
    sys.stdout.flush()

    original_request = req.get("originalRequest")
    if original_request:
        uid = original_request.get("data").get("user").get("userId")
        #logging.info(uid)

    action_handlers = {
        # 'default': None,
        'greetings.start': greeting_handler.process_request,
        # 'aiml.converse': aiml_handler.processRequest,
        'weather.start': weather_handler.process_request
    }

    event = ''
    if action not in action_handlers:
        action = 'default'
        res = req.get("result").get("fulfillment").get("speech")
    else:
        res = action_handlers[action](req)
        event = action.split('.')[0]

    for context in contexts:
        if context.get('name') == "aiml":
            res = aiml_handler.processRequest(req)
            r = prepare_response_string(res)
            return r 

    logging.info("intent:%s" % action)

    r = prepare_response_data(res, event)
    return r

def prepare_response_data(responseData, event):
    responseJson = {
        #"followupEvent": {"name": "WEATHER-RESULT", "data": responseData},
        "followupEvent": {"name": event, "data": responseData},
        # "contextOut": [context], 
        # "data": data,
        "source": "webhook"
    }
    res = json.dumps(responseJson, indent=4)
    res = make_response(res)
    res.headers['Content-Type'] = 'application/json'
    return res

def prepare_response_string(responseString):
    responseJson = {
        "speech": responseString,
        "text": responseString,
        # "data": data,
        # "contextOut": [],
        "source": "webhook"
    } 

    res = json.dumps(responseJson, indent=4)
    res = make_response(res)
    res.headers['Content-Type'] = 'application/json'
    return res

if __name__ == '__main__':
    app.run()

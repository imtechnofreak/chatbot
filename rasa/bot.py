from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import warnings

from rasa_core import utils
from rasa_core.actions import Action
from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.events import SlotSet
from actions.ActionWeather import *
from actions.ActionFamily import *
from actions.ActionStorytelling import *
from actions.ActionRepeat import *
from actions.ActionGreeting import *
from actions.ActionEvent import *
from policies.policy import *

logger = logging.getLogger(__name__)

def train_dialogue(domain_file="domain.yml",
                   model_path="models/dialogue",
                   training_data_file="data/stories.md"):

    policy_ensemble = NewPolicyEnsemble(policies=[MemoizationPolicy(), CustomPolicy(), 
                                                  ElizaPolicy(), TfidfPolicy(), SentimentPolicy()])
    
    agent = Agent(domain_file,
                  policies=policy_ensemble)

    agent.train(
            training_data_file,
            max_history=3,
            epochs=400,
            batch_size=100,
            validation_split=0.2
    )

    agent.persist(model_path)
    return agent


def train_nlu():
    from rasa_nlu.converters import load_data
    from rasa_nlu.config import RasaNLUConfig
    from rasa_nlu.model import Trainer

    training_data = load_data('data/nlu.md')
    trainer = Trainer(RasaNLUConfig("nlu_model_config.json"))
    trainer.train(training_data)
    model_directory = trainer.persist('models/', project_name="nlu", fixed_model_name="current")

    return model_directory


def run(serve_forever=True):
    interpreter = RasaNLUInterpreter("models/nlu/current")
    agent = Agent.load("models/dialogue", interpreter=interpreter)

    if serve_forever:
        input_channel = ConsoleInputChannel()
        agent.handle_channel(input_channel)
    return agent


if __name__ == '__main__':
    utils.configure_colored_logging(loglevel="INFO")

    parser = argparse.ArgumentParser(
            description='starts the bot')

    parser.add_argument(
            'task',
            choices=["train-nlu", "train-dialogue", "run"],
            help="what the bot should do - e.g. run or train?")
    task = parser.parse_args().task

    # decide what to do based on first parameter of the script
    if task == "train-nlu":
        train_nlu()
    elif task == "train-dialogue":
        train_dialogue()
    elif task == "run":
        run()
    else:
        warnings.warn("Need to pass either 'train-nlu', 'train-dialogue' or "
                      "'run' to use the script.")
        exit(1)
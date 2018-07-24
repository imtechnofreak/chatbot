from rasa_core.actions import Action
from models.models import User
from rasa_core.events import SlotSet

class ActionGreeting(Action):
    def name(self):
        return 'action_greeting'

    def run(self, dispatcher, tracker, domain):
        user_id = 0
        user = User(user_id)
        found_user = user.find()[0]
        #dispatcher.utter_message("Greetings, %s!" % (name))
        return [SlotSet("username", found_user['name'] if found_user['name'] is not None else [])]
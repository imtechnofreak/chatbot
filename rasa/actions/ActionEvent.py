from rasa_core.actions import Action
from models.models import User
from rasa_core.events import SlotSet

class ActionEvent(Action):
    def name(self):
        return 'action_event'

    def run(self, dispatcher, tracker, domain):
        user = User(0)
        found_user = user.find()[0]
        events = user.find_events()
        dispatcher.utter_message("Event action!")
        return []
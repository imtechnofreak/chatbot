from rasa_core.actions import Action
from models.models import User
from rasa_core.events import SlotSet

class ActionFamily(Action):
    def name(self):
        return 'action_family'

    def run(self, dispatcher, tracker, domain):
        user = User(0)
        found_user = user.find()[0]
        recent_friends = user.find_most_recent_friend()
        friends_same_city = user.suggest_friends_by_location(found_user['location'])
        dispatcher.utter_message("Family action!")
        return []
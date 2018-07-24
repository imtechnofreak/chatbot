from rasa_core.actions import Action

class ActionStorytelling(Action):
    def name(self):
        return 'action_storytelling'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Storytelling action!")
        return []
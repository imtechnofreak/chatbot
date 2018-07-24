from rasa_core.actions import Action
from rasa_core.events import ActionReverted, UserUtteranceReverted, BotUttered

class ActionRepeat(Action):
    def name(self):
        return 'action_repeat'

    def run(self, dispatcher, tracker, domain):
        command = tracker.get_slot('command')

        if (command == 'help'):
            dispatcher.utter_message('Help command!')
        else:
            #dispatcher.utter_message(dispatcher.latest_bot_messages[-1].text)
            for event in reversed(tracker.events):
                print(event)
                if isinstance(event, BotUttered):
                    dispatcher.utter_message(event.text)
                    break

        return []
from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet, BotUttered


class ActionSayOk(Action):
    def name(self):
        return "action_say_ok"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("OK")
        return [BotUttered("OK")]


class ActionShowEcs(Action):
    def name(self):
        return 'action_show_ecs'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("This is a list of all your ECS")
        return []


class ActionChangeServerState(Action):
    def name(self):
        return "action_change_server_state"

    def run(self, dispatcher, tracker, domain):
        server_name = tracker.get_slot('name')
        dispatcher.utter_message("Server {} state changed".format(server_name))
        return []

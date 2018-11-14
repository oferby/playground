from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet, BotUttered, AllSlotsReset, Restarted
import logging
import pymongo

logger = logging.getLogger(__name__)


def get_client_collection(collection="info"):
    client = pymongo.MongoClient()
    db = client.vca
    return db.get_collection(collection)


def find_all_from_info(type, topic):
    collection = get_client_collection()
    results = collection.find({"type": type, "topic": topic})
    result = []
    for r in results:
        result.append(r)
    return result


def find_one_from_info(type, topic):
    collection = get_client_collection()
    return collection.find_one({"type": type, "topic": topic})


def say(text, dispatcher):
    dispatcher.utter_message(text)


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
        if server_name:
            print('got server name')
            dispatcher.utter_message("Server {} state changed".format(server_name))
            return []
        print('no server name')
        return [SlotSet("isInvalidEntry", "True")]


class ActionClearInvalidEntry(Action):
    def name(self):
        return 'action_clear_invalid_entry'

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("isInvalidEntry", "False")]


class ActionRequestSolution(Action):
    def name(self):
        return 'action_request_solution'

    def run(self, dispatcher, tracker, domain):
        logger.debug('slots: {}'.format(tracker.current_slot_values()))
        say("Let me check for a solution for your needs", dispatcher)
        return []


class ActionRestart(Action):
    def name(self):
        return "action_restart"

    def run(self, dispatcher, tracker, domain):
        return [Restarted()]


class ActionResetSlots(Action):
    def name(self):
        return "action_reset_all_slots"

    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]


class ActionGetInfoFromDb(Action):
    def name(self):
        return "action_query_db"

    def run(self, dispatcher, tracker, domain):
        slots = tracker.current_slot_values()
        logger.debug("slots: {}".format(slots))
        if slots['q_type'] and slots["component"]:
            result = find_one_from_info(slots['q_type'], slots["component"])
            if result:
                say(result['text'], dispatcher)
                return [SlotSet("dbQuerySuccessful", True)]

        return [SlotSet("isInvalidEntry", True)]

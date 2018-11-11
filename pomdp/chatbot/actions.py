from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet, BotUttered, AllSlotsReset, Restarted
import logging

logger = logging.getLogger(__name__)


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


class ActionRequestInformation(Action):
    def name(self):
        return 'action_request_info'

    def run(self, dispatcher, tracker, domain):
        slots = tracker.current_slot_values()
        logger.debug('slots: {}'.format(slots))
        if slots['component']:
            if slots['component'] == 'oss':
                logger.debug("got request for oss information")
                say(
                    "Object Storage Service (OBS) is a stable, secure, efficient, and easy-to-use cloud storage service. With Representational State Transfer Application Programming Interfaces (REST APIs), OBS is able to store unstructured data of any amount and form at 99.999999999% reliability (11 nines).",
                    dispatcher)
                # SlotSet('slot_action_info_ecs', 'True'),
                return [SlotSet("slot_action_info_ok", "True")]
            if slots["component"] == "ecs":
                logger.debug("got request for ecs information")
                say(
                    "An Elastic Cloud Server (ECS) is a computing server consisting of vCPUs, memory, image, and Elastic Volume Service (EVS) disks that allow on-demand allocation and elastic scaling. ECSs integrate Virtual Private Cloud (VPC), virtual firewalls, and multi-data-copy capabilities to create an efficient, reliable, and secure computing environment. This ensures stable and uninterrupted operation of services. After creating an ECS, you can use it like using your local computer or physical server. ECSs support self-service creation, modification, and operation. You can create ECSs by specifying the vCPU, memory, image specifications, and login authentication. After creating an ECS, you can modify its specifications as required.",
                    dispatcher)
                SlotSet('slot_action_info_oss', 'True'),

                return [SlotSet("slot_action_info_ok", "True")]
        return [SlotSet("isInvalidEntry", "True")]


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

from rasa_core_sdk import Action
from rasa_core_sdk.events import *
import logging
import pymongo
from bson.objectid import ObjectId
import numpy as np
from allennlp.predictors.predictor import Predictor
import scipy.stats as sts

logger = logging.getLogger(__name__)


def get_client_collection(collection="info"):
    client = pymongo.MongoClient('10.100.99.85')
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


def add_one(value, collection):
    if collection is not None:
        collection = get_client_collection(collection)
        collection.insert_one(value)


def remove_all(collection):
    if collection is not None:
        collection = get_client_collection(collection)
        collection.remove({})


def say(text, dispatcher):
    dispatcher.utter_message(text)


class ActionUnknownInput(Action):
    def name(self):
        return "action_unknown_input"

    def run(self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
            ):
        logger.debug("writing unknown message to db: {}".format(tracker.latest_message['text']))
        # collection = get_client_collection('unknown_input')
        # doc = {
        #     'user': tracker.sender_id,
        #     'text': tracker.latest_message['text']
        # }
        # collection.insert_one(doc)
        # + json.dumps(tracker.current_state()) + ' , '
        f = open("/tmp/unknown.txt", "a+")
        f.write(tracker.sender_id + ' , ' + tracker.latest_message[
            'text'] + '\n')
        dispatcher.utter_template('utter_default', tracker)
        return [UserUtteranceReverted()]


class ActionUserGoodbye(Action):
    def name(self):
        return "action_user_goodbye"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template('utter_goodbye', tracker)
        return [Restarted()]


class ActionRestart(Action):
    def name(self):
        return "action_restart"

    def run(self, dispatcher, tracker, domain):
        return [Restarted()]


class ActionAdminRestart(Action):
    def name(self):
        return "action_admin_restart"

    def run(self, dispatcher, tracker, domain):
        logger.debug("**** got restart action request. **** ")
        dispatcher.utter_message("session restarted.")
        return [Restarted()]


class ActionResetSlots(Action):
    def name(self):
        return "action_reset_all_slots"

    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]


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


class ActionGetInfoFromDb(Action):
    def name(self):
        return "action_query_db"

    def run(self, dispatcher, tracker, domain):
        slots = tracker.current_slot_values()
        logger.debug("slots: {}".format(slots))
        if slots['q_type'] and slots["component"]:
            result = find_one_from_info(slots['q_type'], slots["component"])
            if result:
                logger.debug("found an answer to: {} {}".format(slots['q_type'], slots["component"]))
                say(result['text'], dispatcher)
                return [SlotSet("dbQuerySuccessful", True)]
        logger.debug("did not find an answer to: {} {}".format(slots['q_type'], slots["component"]))
        return [SlotSet("isInvalidEntry", True)]


class ActionRequestSolution(Action):
    def name(self):
        return 'action_request_solution'

    def run(self, dispatcher, tracker, domain):
        logger.debug('slots: {}'.format(tracker.current_slot_values()))
        say("Let me check for a solution for your needs", dispatcher)
        return []


class ActionCreateEcs(Action):
    def name(self):
        return "action_create_ecs"

    def run(self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
            ):
        slots = tracker.current_slot_values()
        logger.debug("got request for new ecs: {}".format(slots))

        if slots["context_create_ecs"]:
            if slots['image_type']:
                return [SlotSet("context_create_ecs", None), SlotSet("context_create_ecs_done", "5")]
            return [SlotSet("context_create_ecs", str(int(slots["context_create_ecs"]) - 1))]
        say("What image type would you like?", dispatcher)
        return [SlotSet("context_create_ecs", "5")]


class ActionCreateEcsFinalConfirm(Action):
    def name(self):
        return 'action_create_ecs_final_confirm'

    def run(self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
            ):
        slots = tracker.current_slot_values()


class ActionExtractNumOfUsers(Action):
    def name(self):
        return 'action_extract_num_of_users'

    def run(self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
            ):
        slots = tracker.current_slot_values()
        num_of_users = slots['CARDINAL']
        return [SlotSet("q_num_of_users", num_of_users), SlotSet("CARDINAL")]


class ActionTrainingHelp(Action):
    def name(self):
        return 'action_get_training_help'

    def run(self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
            ):
        mgs = 'You can do the following:\n' \
              '* intent list | intents\n' \
              '* '

        say(mgs, dispatcher)
        return [Restarted()]


class ActionGetIntentList(Action):
    def name(self):
        return 'action_get_intents'

    def run(self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
            ):
        logger.debug('getting intent list')
        collection = 'intents'
        collection = get_client_collection(collection)
        intents = collection.find()
        if not intents:
            say('There are no intents to list.', dispatcher)
        else:
            result = []
            for intent in intents:
                result.append(intent['intent'])
            say("intents:\n{}".format(result), dispatcher)
        return [Restarted()]


class ActionAddIntent(Action):
    def name(self):
        return 'action_add_intent'

    def run(self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
            ):
        text = tracker.latest_message['text']
        command = '* addint'

        if text.find(command) == -1:
            say('the command is: * addint', dispatcher)
        else:
            intent = text[len(command) + 1:]
            collection = 'intents'
            collection = get_client_collection(collection)
            collection.insert_one({'intent': intent})
            say('intent added', dispatcher)
        return [Restarted()]


class ActionAskMeSomething(Action):
    def name(self):
        return 'action_ask_me_something'

    def run(self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
            ):

        say("Write a question for the following paragraph.\n"
            "Use '* askme' again to get another question or 'restart' to leave Q&A",
            dispatcher)
        collection = get_client_collection('qanda')
        qanda_list = collection.find()

        ids = []
        text_list = []
        questions = []
        for q in qanda_list:
            text_list.append(q['text'])
            ids.append(q['_id'])
            if 'questions' in q:
                questions.append(q['questions'])
            else:
                questions.append([])

        index = np.random.randint(0, len(ids))
        text = text_list[index]
        id = str(ids[index])
        say(text, dispatcher)

        q_list = questions[index]
        if len(q_list) > 0:
            text = 'I already have the following questions:\n'
            for q in q_list:
                text = text + '\t' + q + '\n'
            text = text + 'so try to give me different question.'
            say(text, dispatcher)

        return [Restarted(), SlotSet("ask_me_something", value=id)]


class ActionGetTrainingQuestion(Action):
    def name(self):
        return 'action_get_training_question'

    def run(self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
            ):
        q_id = tracker.get_slot('ask_me_something')
        q_text = tracker.latest_message['text']

        collection = get_client_collection('qanda')
        qanda = collection.find_one({'_id': ObjectId(q_id)})

        if 'questions' in qanda:
            qs = set(qanda['questions'])
            qs.add(q_text)
            qanda['questions'] = list(qs)

        else:
            qanda['questions'] = [q_text]

        collection.find_one_and_update({'_id': ObjectId(q_id)}, {"$set": qanda},
                                       upsert=False)

        say("Thanks!  if you are still in the mood, run '* askme' again :stuck_out_tongue_winking_eye:", dispatcher)
        return [Restarted()]


class ActionQuestionAnswer(Action):

    def __init__(self):
        self.predictor = Predictor.from_path(
            "data/bidaf-model-2017.09.15-charpad.tar.gz")

    def name(self):
        return 'action_question_answer'

    def run(self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
            ):
        query = tracker.latest_message['text']
        logger.debug('looking for an answer to {}'.format(query))
        collection = get_client_collection('qanda')
        context_list = collection.find()
        answer = {
            "entropy": 20
        }

        for context in context_list:
            text = context['text']
            p = self.predictor.predict(
                passage=text,
                question=query
            )
            p_str = p['span_start_probs']
            p_end = p['span_end_probs']
            p_entropy = (sts.entropy(p_str) + sts.entropy(p_end))/2
            if p_entropy < answer['entropy']:
                answer = p
                answer['entropy'] = p_entropy
            logger.debug('entropy: {}'.format(p_entropy))
        logger.debug('best answer: {}'.format(answer))
        say(answer["best_span_str"], dispatcher)
        return [Restarted()]

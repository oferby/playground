import logging
from pomdp.my_chatbot.nlu import RasaNLUInterpreter

logger = logging.getLogger(__name__)


class SlackAgent:
    def __init__(self, nlu_dir=None):
        self.interpreter = RasaNLUInterpreter(nlu_dir)

    def handle_message(self, message):
        logging.debug("got message from slack: {}".format(message))
        if message['event'] and message['event']['type'] == 'message':
            self.handle_text(message['event'])

    def handle_text(self, message):
        nlu_res = self.interpreter.parse(message['text'])
        logging.debug("NLU result: {}".format(nlu_res))

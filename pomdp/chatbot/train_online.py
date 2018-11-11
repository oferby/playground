from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from rasa_core.channels.slack import SlackInput
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter, EndpointConfig
from rasa_core.training import online

logger = logging.getLogger(__name__)

TOKEN = 'xoxp-331933815733-331258863217-466205375601-9d7740532ac8563ba3305fa2969b8b08'
BOT_TOKEN = 'xoxb-331933815733-467511538663-dEYz2uECXrHqjMf1XlJ7tIiw'
VERIFICATION_TOKEN = 'Z0qtCWe8FPf8NLeuH12UiqZz'

inter = RasaNLUInterpreter("./models/current/nlu")
agent = Agent.load('models/dialogue', interpreter=inter,
                   action_endpoint=EndpointConfig("http://localhost:5055/webhook"))

if __name__ == '__main__':
    slack_input = SlackInput.from_credentials({
        'slack_token': BOT_TOKEN,
        'slack_channel': 'DDQDG62BU'
    })
    online.run_online_learning(agent)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from rasa_core.channels.slack import SlackInput
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter, EndpointConfig


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

TOKEN = 'xoxp-331933815733-331258863217-466127392353-de9b34da0f123c8d7e03d1e3d5264062'
BOT_TOKEN = 'xoxb-331933815733-467511538663-SaCGwmq9hGiOW713QPHuisoU'
VERIFICATION_TOKEN = 'Z0qtCWe8FPf8NLeuH12UiqZz'

inter = RasaNLUInterpreter("./models/current/nlu", "../data/nlu_config.yml")
agent = Agent.load('models/dialogue', interpreter=inter,
                   action_endpoint=EndpointConfig("http://localhost:5055/webhook"),
                   )

if __name__ == '__main__':
    slack_input = SlackInput.from_credentials({
        'slack_token': BOT_TOKEN,
        'slack_channel': 'DDQDG62BU'
    })
    logger.debug('starting channel....')
    agent.handle_channels([slack_input], 5051)

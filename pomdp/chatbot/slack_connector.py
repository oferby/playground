from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from rasa_core.channels.slack import SlackInput
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter, EndpointConfig

from vca.policy import PomdpPolicy
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename='anan.log',
                    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S')

TOKEN = 'xoxp-'
BOT_TOKEN = 'xoxb-'
VERIFICATION_TOKEN = 'Z0q'

inter = RasaNLUInterpreter("./models/current/nlu", "../data/nlu_config.yml")
agent = Agent.load('models/dialogue', interpreter=inter,
                   action_endpoint=EndpointConfig("http://localhost:5055/webhook"),
                   )

if __name__ == '__main__':
    slack_input = SlackInput.from_credentials({
        'slack_token': BOT_TOKEN,
        'slack_channel': 'DD'
    })
    logger.debug('starting channel....')
    agent.handle_channels([slack_input], 5051)

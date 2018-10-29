from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from flask import Blueprint, request, jsonify

from rasa_core.channels.slack import SlackBot, SlackInput
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter, EndpointConfig

logger = logging.getLogger(__name__)

TOKEN = 'xoxp-331933815733-331258863217-465852994305-a6d46121f556626202ec6ed7832d502e'
BOT_TOKEN = 'xoxb-331933815733-467511538663-8aCE9IY1XxcUw8rb1OnoeLTy'
VERIFICATION_TOKEN = 'Z0qtCWe8FPf8NLeuH12UiqZz'

# slack_bot = SlackBot(BOT_TOKEN)
inter = RasaNLUInterpreter("./models/current/nlu")
agent = Agent.load('models/dialogue', interpreter=inter,
                   action_endpoint=EndpointConfig("http://localhost:5055/webhook"))

# 'Z0qtCWe8FPf8NLeuH12UiqZz'

if __name__ == '__main__':
    slack_input = SlackInput.from_credentials({
        'slack_token': BOT_TOKEN,
        'slack_channel': 'DDQDG62BU'
    })
    agent.handle_channels([slack_input], 5051)
    # slack_input.blueprint(process_message)

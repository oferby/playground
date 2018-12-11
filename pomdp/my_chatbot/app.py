from flask import Flask, Blueprint, request, jsonify, make_response, Response
from slackclient import SlackClient
import json
import pomdp.my_chatbot.agent as agent
import logging

BOT_TOKEN = 'xoxb-331933815733-467511538663-HHotuujBTiXKgpB0d5B8v7RX'
SLACK_CHANNEL = 'DDQDG62BU'
VERIFICATION_TOKEN = 'Z0qtCWe8FPf8NLeuH12UiqZz'

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def send_to_slack(text):
    c = SlackClient(BOT_TOKEN)
    r = c.api_call(
        "chat.postMessage",
        channel=SLACK_CHANNEL,
        text="Hello from client"

    )
    print(r)


def blueprint():
    slack_webhook = Blueprint('slack_webhook', __name__)
    slack_agent = agent.SlackAgent('../chatbot/models/current/nlu')

    @slack_webhook.route("/", methods=['GET'])
    def health():
        return jsonify({"status": "ok"})

    @slack_webhook.route("/webhooks/slack/webhook", methods=['GET', 'POST'])
    def webhook():
        request.get_data()
        if request.json:
            output = request.json
            print("request: {}".format(output))

            if output['token'] != VERIFICATION_TOKEN:
                logging.error("got message with wrong token")
                return

            if "challenge" in output:
                return make_response(output.get("challenge"), 200,
                                     {"content_type": "application/json"})

            slack_agent.handle_message(output)

        elif request.form:
            output = dict(request.form)
            print(output)

        return make_response()

    return slack_webhook


app = Flask("VCA")
app.register_blueprint(blueprint())
app.run(port=5051)

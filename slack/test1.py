from flask import Flask, request
from slackclient import SlackClient

BOT_TOKEN = 'xoxb-...'
SLACK_CHANNEL = '...'

c = SlackClient(BOT_TOKEN)

r = c.api_call(
    "chat.postMessage",
    channel=SLACK_CHANNEL,
    text="Hello from client"

)
print(r)

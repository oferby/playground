from rasa_core.interpreter import RasaNLUInterpreter, EndpointConfig
import json
from rasa_core.agent import Agent
from rasa_core.channels import UserMessage
from rasa_core.tracker_store import MongoTrackerStore
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy

inter = RasaNLUInterpreter("./models/current/nlu")
agent = Agent.load('models/dialogue', interpreter=inter,
                   action_endpoint=EndpointConfig("http://localhost:5055/webhook"),
                   tracker_store=MongoTrackerStore(
                       None,
                       host="mongodb://10.100.99.85:27017")
                   )

print('listening...')
result = "hello there"
    # input()

while result:
    responses = agent.handle_message(UserMessage(result))
    for r in responses: print(r)
    result = input()

# message = "I need virtual server"
# result = interpreter.parse(message)
# print(json.dumps(result, indent=2))

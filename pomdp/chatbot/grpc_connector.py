from concurrent import futures
import time

import logging
from rasa_core.agent import Agent
from rasa_core.channels import UserMessage
from rasa_core.interpreter import RasaNLUInterpreter, EndpointConfig
from rasa_core.tracker_store import MongoTrackerStore

import grpc
import sys

sys.path.insert(0, "./protos")

import chat_pb2 as pb2
import chat_pb2_grpc as pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename='/tmp/anan.log',
                    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S')


class ChatServiceServicer(pb2_grpc.ChatServiceServicer):

    def __init__(self):
        inter = RasaNLUInterpreter("./models/current/nlu", "./data/nlu_config.yml")
        self.agent = Agent.load('models/dialogue', interpreter=inter,
                                tracker_store=MongoTrackerStore(
                                    None,
                                    host="mongodb://10.100.99.85:27017"),
                                action_endpoint=EndpointConfig("http://localhost:5055/webhook"))

    def getChatResponse(self, request, context):
        logger.debug('got request: {}'.format(request.text))
        responses = self.agent.handle_message(UserMessage(request.text))
        logger.debug('responses: {}'.format(responses))
        return pb2.ChatResponse(text=responses[0]['text'])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    pb2_grpc.add_ChatServiceServicer_to_server(ChatServiceServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print('server started.')
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()

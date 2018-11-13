import grpc
import pomdp.chatbot.protos.actions_pb2 as pd2
import pomdp.chatbot.protos.actions_pb2_grpc as pd2_grpc


def send_action(action_req):

    with grpc.insecure_channel('10.10.11.146:50051') as channel:
        stub = pd2_grpc.CloudActionServiceStub(channel)
        res = stub.getAction(pd2.CloudActionRequest(action=action_req))
        print('res: {}'.format(res.response))


if __name__ == '__main__':
    send_action('test_action')


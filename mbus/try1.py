import queue
import threading


class Producer:
    def __init__(self, q, i):
        self.q = q
        self.my_q = queue.Queue()
        self.index = i

    def produce(self):
        task = {"q": self.my_q, "task": "task_{}".format(self.index)}
        self.q.put(task)
        task = self.my_q.get(True)
        print(task)

class ConsumerThread(threading.Thread):

    def __init__(self, q):
        self.q = q
        self.consumer_index = 100
        super(ConsumerThread, self).__init__()

    def run(self):
        while True:
            task = self.q.get(True)

            self.consumer_index += 1
            task['task'] = task['task'] + '_' + str(self.consumer_index)
            task['q'].put(task)

main_q = queue.Queue()
consumer = ConsumerThread(main_q)
consumer.start()

for i in range(10):
    p = Producer(main_q, i)
    p.produce()

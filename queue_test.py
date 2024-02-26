import hazelcast
import threading
import time

client = hazelcast.HazelcastClient(cluster_name="dev",)
my_queue = client.get_queue("queue").blocking()
my_queue.clear()


def produce():
    for i in range(100):
        if my_queue.offer(i):
            print(f'Added {i}; size = {my_queue.size()}')
        else:
            print(f'Could not add {i}')
        time.sleep(0.5)


def consume(queue, id):
    while True:
        head = queue.poll(1)
        if head is not None:
            print(id, "thread consumed {}".format(head))
        time.sleep(2)


producer_thread = threading.Thread(target=produce)
producer_thread.start()

consumer_thread_1 = threading.Thread(target=consume, args=(my_queue, 1))
consumer_thread_1.start()

consumer_thread_2 = threading.Thread(target=consume, args=(my_queue, 2))
consumer_thread_2.start()

producer_thread.join()
consumer_thread_1.join()
consumer_thread_2.join()

client.shutdown()

import sys, threading, hazelcast
from flask import Flask

app = Flask(__name__)
messages = []


def read_queue():
    def consume():
        while True:
            message = queue.take()['msg']
            if message is not None:
                messages.append(message)
                print(message)

    client = hazelcast.HazelcastClient(cluster_name="dev")
    queue = client.get_queue("queue").blocking()
    consumer_thread = threading.Thread(target=consume)
    consumer_thread.start()


@app.route('/get_static_message', methods=['GET'])
def get_static_message():
    return ", ".join(messages)


if __name__ == '__main__':
    read_queue()
    port = 8085 + int(sys.argv[1])
    app.run(port=port)

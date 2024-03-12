from flask import Flask, request, make_response
import hazelcast, sys

app = Flask(__name__)

member_port = 5701
member_port += int(sys.argv[1])
client = hazelcast.HazelcastClient(
    cluster_name="dev",
    cluster_members=[
        "127.0.0.1:" + str(member_port),
    ]
)

messages = client.get_map("my-map").blocking()


@app.route('/log_message', methods=['POST'])
def log_message():
    data = request.get_json()
    messages.put(data['UUID'], data['msg'])
    print(data['msg'])
    return make_response(' ', 200)


@app.route('/get_all_messages', methods=['GET'])
def get_all_messages():
    return ", ".join(messages.values())


if __name__ == '__main__':
    port = 8082
    port += int(sys.argv[1])
    app.run(debug=True, port=port)

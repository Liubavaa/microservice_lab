from flask import Flask, request, make_response
import requests, uuid, random, hazelcast

app = Flask(__name__)

client = hazelcast.HazelcastClient(cluster_name="dev")
queue = client.get_queue("queue").blocking()


logging_service_urls = ["http://localhost:8082", "http://localhost:8083", "http://localhost:8084"]
messages_service_urls = ["http://localhost:8085", "http://localhost:8086"]


@app.route('/post_message', methods=['POST'])
def post_message():
    msg = request.get_json()
    unique_id = str(uuid.uuid4())
    logging_data = {"UUID": unique_id, "msg": msg}
    queue.add(logging_data)
    response = requests.post(random.choice(logging_service_urls) + "/log_message", json=logging_data)
    return make_response(response.text, response.status_code)


@app.route('/get_messages', methods=['GET'])
def get_messages():
    logging_response = requests.get(random.choice(logging_service_urls) + "/get_all_messages")
    messages_response = requests.get(random.choice(messages_service_urls) + "/get_static_message")
    return logging_response.text + ": " + messages_response.text


if __name__ == '__main__':
    app.run(debug=True, port=8080)

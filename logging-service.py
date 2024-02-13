from flask import Flask, request, make_response

app = Flask(__name__)

messages = {}


@app.route('/log_message', methods=['POST'])
def log_message():
    data = request.get_json()
    messages[data['UUID']] = data['msg']
    print(data['msg'])
    return make_response(' ', 200)


@app.route('/get_all_messages', methods=['GET'])
def get_all_messages():
    return ", ".join(messages.values())


if __name__ == '__main__':
    app.run(debug=True, port=8082)

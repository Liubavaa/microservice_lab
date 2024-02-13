from flask import Flask
app = Flask(__name__)


@app.route('/get_static_message', methods=['GET'])
def get_static_message():
    return "Not implemented yet"


if __name__ == '__main__':
    app.run(debug=True, port=8081)

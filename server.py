from flask import Flask, request
from main import predict

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, welcome to my Flask server!'

@app.route('/post_example', methods=['POST'])
def post_example():
    if request.method == 'POST':
        # Access the data sent in the POST request
        data = request.get_json()  # Assuming the data is sent as JSON
        # You can also use request.form to get form data
        # data = request.form

        # Process the data
        # For example, if the JSON contains a key 'message'
        if 'question' in data:
            received_message = data['question']
            o=predict(received_message)

            return f"Received message: {o}"
        else:
            return "No 'message' key found in the POST request data"
    else:
        return "This endpoint only accepts POST requests"

if __name__ == '__main__':
    app.run(debug=True)

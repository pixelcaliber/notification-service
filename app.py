from threading import Thread

from confluent_kafka import Consumer, KafkaError, Producer
from flask import Flask, json, jsonify, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)


@socketio.on("connect")
def handle_connect():
    print("Client Connected")


consumer_config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "my_consumer_group",
    "auto.offset.reset": "earliest",
}
consumer = Consumer(consumer_config)
consumer.subscribe(["received_messages"])


# Kafka consumer loop
def kafka_consumer():
    while True:
        msg = consumer.poll(10000)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        # Log received message
        kafka_message = msg.value().decode("utf-8")
        # Parse the JSON string into a Python dictionary

        kafka_message_dict = json.loads(kafka_message)

        print("Received Kafka message:", kafka_message_dict)

        # Emit message to WebSocket clients
        socketio.emit("new_message", kafka_message_dict)


# Start Kafka consumer in a separate thread
kafka_thread = Thread(target=kafka_consumer)
kafka_thread.start()


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    socketio.run(app, port=8000, debug=True)


# # Kafka producer setup
# producer_config = {'bootstrap.servers': 'localhost:9092'}
# producer = Producer(producer_config)
# # Route to send a new message
# @app.route('/api/send_message', methods=['POST'])
# def send_message():
#     try:
#         data = request.json
#         username = data.get('username')

#         if username:
#             # Publish the message to the 'received_messages' topic
#             kafka_message = {
#                 'username': username
#             }
#             producer.produce('received_messages', value=json.dumps(kafka_message))
#             producer.flush()

#             # socketio.emit('new_message', kafka_message)

#             return jsonify({'status': 'success', 'message': 'Message sent successfully!'})

#         else:
#             return jsonify({'status': 'error', 'message': 'Invalid request format'}), 400

#     except Exception as e:
#         print(f"Error sending message: {e}")
#         return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

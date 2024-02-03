# notification-service

Part of chat-application microservices: Kafka Consumer loop a "worker" running infintely and listening to kafka topic through long pooling (pool time: 1000ms)
- whenever a new message arrives in the Kafka topic Consumer loop consumes that message
- A websocket connection is established with the client to push them as notifications which creates alert messages client-side (react-js application).
- The new kafka messages are processed and delivered to firebase to create notification in client devices using FCMs

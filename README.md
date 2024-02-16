# notification-service

Part of chat-application microservices: Kafka Consumer loop a "worker" running infintely and listening to kafka topic through long pooling (pool time: 1000ms)
- whenever a new message arrives in the Kafka topic Consumer loop consumes that message
- A websocket connection is established with the client to push them as notifications which creates alert messages client-side (react-js application).
- The new kafka messages are processed and delivered to firebase to create notification in client devices using FCMs

tech-stack: Kafka, Python, Flask, Firebase, Worker, Websockets, Kafka Streams

### More details:

- Adopting the Producer/Consumer pattern offers a solution for decoupling processes involved in producing and consuming notifications, especially when these processes operate at different rates. Utilizing Kafka, a scalable message broker, becomes advantageous, particularly when dealing with large volumes of data and high loads.
- Notifications, which are events triggered by various actions within the web application such as user registration or message sending, will be generated and published to designated topics.
- A consumer component is implemented to subscribe to these events, processing them through Firebase Cloud Messaging (FCM) to generate notifications within the web application.
- Firebase Cloud Messaging is used to create notification using the FCM Tokens which are unique per device to the consumer devices.


### Apache Kafka
Kafka is a distributed event streaming platform that lets you read, write, store, and process events (also called records or messages in the documentation) across many machines.
The purpose of Kafka in the solution is to decouple producer (database) and consumer (which can be multiple) and to be able to scale to millions of events or notifications. It provides a free flow of data into topics which can be extracted, transformed and loaded into multiple sinks. 
Different topics can be created for different use cases to store events such new user registration or new messages, and any number of sinks can subscribe to the topics for ingesting data.

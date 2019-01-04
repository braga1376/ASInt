async function createSubscription(topicName, subscriptionName) {
  // [START pubsub_create_pull_subscription]
  // Imports the Google Cloud client library
  const {PubSub} = require('@google-cloud/pubsub');

  const pubsub = new PubSub();
  //const topicName = "{{username}}";
  //const subscriptionName = "{{username}}-client";

  // Creates a new subscription
  await pubsub.topic(topicName).createSubscription(subscriptionName);
  console.log(`Subscription ${subscriptionName} created.`);

  // [END pubsub_create_pull_subscription]
}

function listenForMessages(subscriptionName) {
  const {PubSub} = require('@google-cloud/pubsub');

  // Creates a client
  const pubsub = new PubSub();

  const timeout = 60;

  // References an existing subscription
  const subscription = pubsub.subscription(subscriptionName);

  // Create an event handler to handle messages
  let messageCount = 0;
  const messageHandler = message => {
    console.log(`Received message ${message.id}:`);
    console.log(`\tData: ${message.data}`);
    console.log(`\tAttributes: ${message.attributes}`);
    messageCount += 1;

    // "Ack" (acknowledge receipt of) the message
    message.ack();
  };
    // Listen for new messages until timeout is hit
  subscription.on(`message`, messageHandler);

  setTimeout(() => {
    subscription.removeListener('message', messageHandler);
    console.log(`${messageCount} message(s) received.`);
  }, timeout * 1000);
  // [END pubsub_subscriber_async_pull]
  // [END pubsub_quickstart_subscriber]
}
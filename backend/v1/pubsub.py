
from handle_task import process_task
import os
from google.cloud import pubsub_v1
import json


TOPIC = os.getenv("PUBSUB_TOPIC", "projects/elegant-cipher-378223/topics/conversion.request-sub")
SUBSCRIPTION_NAME = os.getenv("PUBSUB_SUBSCRIPTION", "projects/elegant-cipher-378223/subscriptions/conversion.request-sub-sub")
publisher = pubsub_v1.PublisherClient()

def publish_task(id_task):
    message = json.dumps({"id_task": id_task}).encode("utf-8")
    publisher.publish(TOPIC, message)

def callback(message):
    print(message)
    id_task = json.loads(message.data.decode("utf-8"))["id_task"]
    try:
        process_task(id_task)
        message.ack()
    except Exception as e:
        print(e)
        message.nack()

if __name__ == "__main__":
    with pubsub_v1.SubscriberClient() as subscriber:
        future = subscriber.subscribe(SUBSCRIPTION_NAME, callback)
        try:
            future.result()
        except KeyboardInterrupt:
            future.cancel()
        
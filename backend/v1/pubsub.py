
from handle_task import process_task
import os
from google.cloud import pubsub_v1
import json
import uvicorn
from fastapi import FastAPI, Request
import base64

app = FastAPI()

## Cloud run pubsub trigger
@app.post("/")
async def trigger(request: Request):
    ## get the id_task from the request
    envelop = await request.json()
    print(envelop)

    b64_data = envelop["message"]["data"]
    str_data = base64.b64decode(b64_data).decode("utf-8")
    json_data = json.loads(str_data)
    id_task = json_data["id_task"]
    ## call the process_task function
    process_task(id_task)
    ## it should return a 200 status code
    return {"status": "ok"}


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
    PUBSUB_EXECUTION = os.getenv("PUBSUB_EXECUTION", "trigger")
    if PUBSUB_EXECUTION == "trigger":
        print("Starting trigger")
        uvicorn.run(app, host="0.0.0.0", port=8080)
    elif PUBSUB_EXECUTION == "subscriber":             
        print("Starting subscriber")
        with pubsub_v1.SubscriberClient() as subscriber:
            future = subscriber.subscribe(SUBSCRIPTION_NAME, callback)
            try:
                future.result()
            except KeyboardInterrupt:
                future.cancel()
        
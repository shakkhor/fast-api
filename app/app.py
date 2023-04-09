from fastapi import FastAPI
import boto3
from pydantic import BaseModel

class Message(BaseModel):
    message: str
    queue: str


class Queue(BaseModel):
    name: str


app = FastAPI()

@app.get("/", tags=['ROOT'])
async def root() -> dict:
    return{"ping":"pong"}

@app.post("/send", tags=['ROOT'])
async def send(message: Message):
    sqs = boto3.client('sqs', endpoint_url='http://localhost:4566')
    queue_url = 'http://localhost:4566/queue/'+message.queue
    response = sqs.send_message(QueueUrl=queue_url, MessageBody=message.message)
    return response


@app.post("/create", tags=['ROOT'])
async def create(queue: Queue):
    sqs = boto3.client('sqs', endpoint_url='http://localhost:4566', )
    queue_name = queue.name
    response = sqs.create_queue(QueueName=queue_name)
    print(response)
    
    return response

@app.get("/list-queues", tags=['ROOT'])
async def get_queues(prefix=None):
    sqs = boto3.client('sqs', endpoint_url='http://localhost:4566', )

    if prefix:
        queue_iter = sqs.list_queues(QueueNamePrefix=prefix)
    else:
        queue_iter = sqs.list_queues()
    queues = list(queue_iter)

    return queue_iter

@app.get("/check-messages", tags=['ROOT'])
async def check_messages(queue: str):
    queue_url = 'http://localhost:4566/queue/'+queue
    sqs = boto3.client('sqs', endpoint_url='http://localhost:4566', )
    return sqs.receive_message(QueueUrl=queue_url)




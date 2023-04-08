from fastapi import FastAPI
import boto3
app = FastAPI()

@app.get("/", tags=['ROOT'])
async def root() -> dict:
    return{"ping":"pong"}

@app.post("/send", tags=['ROOT'])
async def send():
    sqs = boto3.client('sqs', endpoint_url='http://localhost:4566')
    queue_url = 'http://localhost:4566/queue/test-queue'
    response = sqs.send_message(QueueUrl=queue_url, MessageBody='chola muri peyaji beguni alur chop')
    return response


@app.get("/create", tags=['ROOT'])
async def create():
    sqs = boto3.client('sqs', endpoint_url='http://localhost:4566', )
    queue_name = 'test-queue'
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
async def check_messages():
    queue_url = 'http://localhost:4566/queue/test-queue'
    sqs = boto3.client('sqs', endpoint_url='http://localhost:4566', )
    return sqs.receive_message(QueueUrl=queue_url)




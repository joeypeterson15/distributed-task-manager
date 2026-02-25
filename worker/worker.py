import sys
import os
from dotenv import load_dotenv
import json
import websockets
import asyncio

URI = 'ws://localhost:8001'
load_dotenv()
port = os.getenv("PORT")

MESSAGE = {
    'register' : {
        'type': 'register',
        'payload': {
            'name': 'worker',
            'id': ''
        }
    },

    'stdout' : {
        'type': 'stdout',
        'payload': {
            'message': ''
        } 
    }
}

class Worker():
    def __init__(self, id):
        self.id = id

    async def connect(self):
        async with websockets.connect(URI) as websocket:
            await self.send(websocket, 'register', **{'id': f'{self.id}'})

            while True:
                message = await websocket.recv()
                message = json.loads(message)

                if message['type'] == 'task_assign':
                    self.task = message['payload']['task']
                    self.meta = message['payload']['meta']
                    self.process_task()
                    await self.send(websocket, 'stdout', **{'message': f'Worker {self.id} Processing task: {message['payload']['task']}'})

    def process_task(self):
        dims = self.meta['region_precision']
        # this is where we start writing heat equation code.
        # the worker should not need to know about how to do the calculations. It can call another class for that.
    
    async def send(self, websocket, type, **kwargs):
        message = MESSAGE[type]
        for key in kwargs.keys():
            message['payload'][key] = kwargs[key]
        await websocket.send(json.dumps(message))


async def gen_workers(n):
    workers = []
    for id in range(n):
        w = Worker(id)
        workers.append(w.connect())
    await asyncio.gather(*workers)


if __name__ == "__main__":
    n_workers = 1
    if len(sys.argv) > 1:
        n_workers = int(sys.argv[1])
    
    asyncio.run(gen_workers(n_workers))

import sys
import os
from dotenv import load_dotenv
import json
import websockets
import asyncio
import heat
import concurrent.futures
import numpy as np

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
    },

    'task_complete' : {
        'type': 'task_complete',
        'payload': {
            'new_region': ''
        }
    },

    'task_request' : {
        'type': 'task_request',
        'payload': {

        }
    }
}

class Worker():
    def __init__(self, id):
        self.id = id

    async def connect(self, executor):
        async with websockets.connect(URI) as websocket:
            await self.send(websocket, 'register', **{'Worker Id': f'{self.id}'})
            await self.request_task(websocket)

            while True:
                try:
                    response_raw = await asyncio.wait_for(
                        websocket.recv(),
                        timeout=2.0
                    )
                    message = json.loads(response_raw)

                    if message['type'] == 'task_assign':
                        loop = asyncio.get_running_loop()
                        new_region = await loop.run_in_executor(
                            executor,
                            self.process_task,
                            message['payload']
                        )
                        payload = {
                            'region_vals': new_region.tolist(),
                            'region': message['payload']['region'],
                            'epoch': message['payload']['epoch']
                            }
                        await self.send(websocket, 'task_complete', **payload)
                        await self.send(websocket, 'task_request')

                except asyncio.TimeoutError:
                    await self.send(websocket, 'task_request')

    def process_task(self, payload):
        updated_region = heat.update_region(payload)
        return updated_region
    
    async def request_task(self, websocket):
        await self.send(websocket, 'task_request')

    
    async def send(self, websocket, type, **kwargs):
        message = MESSAGE[type]
        for key in kwargs.keys():
            message['payload'][key] = kwargs[key]
        await websocket.send(json.dumps(message))


async def gen_workers(n, executor):
    workers = []
    for id in range(n):
        w = Worker(id)
        workers.append(w.connect(executor))
    await asyncio.gather(*workers)


if __name__ == "__main__":
    n_workers = 1
    if len(sys.argv) > 1:
        n_workers = int(sys.argv[1])
    executor = concurrent.futures.ProcessPoolExecutor()
    asyncio.run(gen_workers(n_workers, executor))

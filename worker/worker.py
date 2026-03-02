import sys
import os
from dotenv import load_dotenv
import json
import websockets
import asyncio
import heat
import multiprocessing
import concurrent.futures

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
}

class Worker():
    def __init__(self, id):
        self.id = id

    async def connect(self, executor):
        async with websockets.connect(URI) as websocket:
            await self.send(websocket, 'register', **{'id': f'{self.id}'})

            while True:
                message = await websocket.recv()
                message = json.loads(message)

                if message['type'] == 'task_assign':
                    loop = asyncio.get_running_loop()
                    await self.send(websocket, 'stdout', **{'message': f'Worker {self.id} Processing task'})
                    new_region = await loop.run_in_executor(
                        executor,
                        self.process_task,
                        message['payload']
                    )
                    await self.send(websocket, 'task_complete', **{'region': new_region.tolist(), 'region_coords': message['payload']['region_coords']})


    def process_task(self, payload):
        grid = payload['grid']
        region_coords = payload['region_coords']
        n_regions = payload['n_regions']
        n_cells = payload['n_cells']
        return heat.update_region(grid, region_coords, n_regions, n_cells)
    
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

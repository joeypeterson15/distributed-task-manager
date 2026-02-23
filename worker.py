import sys
import requests
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
            'id': None
        }
    }
}

class Worker():
    def __init__(self, id):
        self.id = id
        self.status = -1

    async def connect(self):
        async with websockets.connect(URI) as websocket:
            await self.register(websocket)

            while True:
                message = await websocket.recv()
                print(f"Server: {message}")

    async def register(self, websocket):
        payload = MESSAGE['register']
        payload['payload']['id'] = self.id
        payload = json.dumps(payload)
        await websocket.send(payload)

async def gather_workers(n):
    await asyncio.gather(create_workers(n))

async def create_workers(n):
    for id in range(n):
        w = Worker(id)
        await w.connect()

if __name__ == "__main__":
    n_workers = 1
    if len(sys.argv) > 1:
        n_workers = int(sys.argv[1])
    
    asyncio.run(gather_workers(n_workers))

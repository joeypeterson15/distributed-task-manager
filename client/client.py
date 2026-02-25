import os
from dotenv import load_dotenv
import websockets
import asyncio
import json
import sys

load_dotenv()
port = os.getenv("PORT")

URI = 'ws://localhost:8001'
MESSAGE = {
    'register' : {
        'type': 'register',
        'payload': {
            'name': 'client',
            'tasks': None,
            'id': None
        }
    }
}

class Client():
    def __init__(self, tasks):
        self.id = 23
        self.tasks = tasks

    async def connect(self):
        async with websockets.connect(URI) as websocket:
            await self.register(websocket)

            while True:
                message = await websocket.recv()
                print(f"Server: {message}")
    
    async def register(self, websocket):
        payload = MESSAGE['register']
        payload['payload']['id'] = self.id
        payload['payload']['tasks'] = self.tasks
        payload = json.dumps(payload)
        await websocket.send(payload)

if __name__ == "__main__":
    tasks = sys.argv[1]

    client = Client(tasks)
    asyncio.run(client.connect())
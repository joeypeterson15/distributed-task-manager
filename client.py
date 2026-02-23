import cmd
import requests
import os
from dotenv import load_dotenv
import websockets
import asyncio
import json

load_dotenv()
port = os.getenv("PORT")

URI = 'ws://localhost:8001'
MESSAGE = {
    'register' : {
        'type': 'register',
        'payload': {
            'name': 'client',
            'id': None
        }
    }
}

class Client():
    def __init__(self):
        self.id = 23

    async def connect(self):
        async with websockets.connect(URI) as websocket:
            payload = MESSAGE['register']
            payload['payload']['id'] = self.id
            payload = json.dumps(payload)
            await websocket.send(payload)

            message = await websocket.recv()
            print(f"Server: {message}")

if __name__ == "__main__":
    client = Client()
    asyncio.run(client.connect())
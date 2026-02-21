import sys
import requests
import os
from dotenv import load_dotenv
import json
import websockets
import asyncio

load_dotenv()
port = os.getenv("PORT")

class Worker():
    def __init__(self, id):
        self.id = id
        self.status = -1
        # self.registerWithScheduler()


    async def registerWithScheduler(self):
        # payload = {'id' : self.id}
        uri = 'ws://localhost:8001'
        async with websockets.connect(uri) as websocket:
        # Send a message to the server
            await websocket.send(f'{self.id}')

        # Receive a response from the server
            message = await websocket.recv()
            print(f"Received: {message}")


async def create_workers(n):
    # for id in range(n):
    #     w = Worker(id)
    for id in range(n):
        w = Worker(id)
        await w.registerWithScheduler()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        n_workers = int(sys.argv[1])
        asyncio.run(create_workers(n_workers))

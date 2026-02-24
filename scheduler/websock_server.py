import websockets
import asyncio
from websockets.asyncio.server import serve
from scheduler_class import Scheduler
import json

async def server():
    scheduler = Scheduler()

    async def handler(websocket):
        while True:
            message = json.loads(await websocket.recv())
            type, payload  = message['type'], message['payload']
            if type == 'register':
                await register(websocket,payload)

    async def register(websocket,payload):
        name,id = payload['name'], payload['id']

        if name == 'worker':
            scheduler.register_worker(id)
            print(f'Worker {id}: Registered')

        if name == 'client':
            tasks = payload['tasks']
            scheduler.register_client(id)
            await websocket.send(f'Client Registered')
            scheduler.register_tasks(tasks)
            await websocket.send(f'Tasks Registered')
         

    async def main():
        async with serve(handler, "", 8001) as server:
            await server.serve_forever()
    
    await main()

if __name__ == "__main__":
    s = Scheduler()
    asyncio.run(server())


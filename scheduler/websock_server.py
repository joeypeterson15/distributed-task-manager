import websockets
import asyncio
from websockets.asyncio.server import serve
from scheduler_class import Scheduler
import json

MESSAGE = {
    'task_assign' : {
        'type': 'task_assign',
        'payload': {
            'task': '12345'
        } 
    }
}

async def server():
    scheduler = Scheduler()

    async def handler(websocket):
        while True:
            message = json.loads(await websocket.recv())
            type, payload  = message['type'], message['payload']
            if type == 'register':
                await register(websocket, payload)
                # now we need the dependency tree ready so that as each worker registers we can start assigning tasks to it.
                await send(websocket, 'task_assign')
            if type == 'stdout':
                print(f'{payload['message']}')

    async def register(websocket,payload):
        name,id = payload['name'], payload['id']

        if name == 'worker':
            scheduler.register_worker(websocket)
            print(f'Worker {id}: Registered')

        if name == 'client':
            tasks = payload['tasks']
            scheduler.register_client(websocket)
            await websocket.send(f'Client Registered')
            scheduler.register_tasks(tasks)
            await websocket.send(f'Tasks Registered')
         
    async def send(websocket, type, **kwargs):
        message = MESSAGE[type]
        for key in kwargs.keys():
            message['payload'][key] = kwargs[key]
        await websocket.send(json.dumps(message))

    async def main():
        async with serve(handler, "", 8001) as server:
            await server.serve_forever()
    
    await main()

if __name__ == "__main__":
    s = Scheduler()
    asyncio.run(server())


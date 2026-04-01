import websockets
import asyncio
from websockets.asyncio.server import serve
from scheduler_class import Scheduler
import json
import visualizer
import numpy as np
import os
import time

MESSAGE = {
    'task_assign' : {
        'type': 'task_assign',
        'payload': {} 
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

            if type == 'stdout':
                print(f'{payload['message']}')

            if type == 'task_complete':
                # print('region:', payload['region'])
                # print('epoch: ', payload['epoch'])
                print(f'task complete')
                await update_grid(payload)
            
            if type == 'task_request':
                # print(f'task request')
                if scheduler.tasks_queue:
                    # print('len scheduler queue', len(scheduler.tasks_queue), websocket)
                    await assign_task(websocket)

    
    async def update_grid(payload):
        region = payload['region']
        epoch = payload['epoch']
        region_vals = np.array(payload['region_vals'], dtype='float32')

        scheduler.update_grid(region, region_vals, epoch)
        if np.all(scheduler.prev_region_present[epoch]):
            print(np.sum(scheduler.grid[epoch]))
            # print(f'EPOCH {epoch} COMPLETE: REGION VALUES: => ', scheduler.grid[epoch])
        if np.all(scheduler.prev_region_present[scheduler.epochs - 1]):
            visualizer.visualize(scheduler.grid)
            return
        if epoch < scheduler.epochs - 1:
            scheduler.increment_dependents_and_enqueue(region, epoch)


    async def assign_task(websocket):
        task = scheduler.tasks_queue.popleft()
        await send(websocket, 'task_assign', **task)

    async def register(websocket, payload):
        name,id = payload['name'], payload['id']

        if name == 'worker':
            scheduler.register_worker(websocket, id)
            print(f'Worker {id}: Registered')

        if name == 'client':
            tasks = payload['tasks']
            scheduler.register_client(websocket)
            await websocket.send(f'Client Registered')
            scheduler.configure_tasks(tasks)
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
    asyncio.run(server())


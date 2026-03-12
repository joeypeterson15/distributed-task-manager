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
                await update_grid(payload)


    async def update_grid(payload):
        region_coords = payload['region_coords']
        new_region = np.array(payload['region'], dtype='float32')

        scheduler.update_grid(region_coords, new_region)
        scheduler.n_worker_updates += 1
        # INSTEAD OF SENDING UPDATES WHEN ALL WORKERS ARE DONE
        #   CHECK IF THE WORKERS BOUNDARIES ARE PRESENT
        #       IF WORKERS BOUNDARIES ARE UPDATED THEN UPDATE REGION BOUNDARIES AND GRID AND SEND NEIGHBOR BOUNDARIES BACK
        #       ELSE JUST UPDATE REGION BOUNDARIES AND CONTINUE LISTENING
        if scheduler.n_worker_updates == scheduler.n_regions:
            print(f'Epoch {scheduler.epoch + 1} Complete')
            scheduler.n_worker_updates = 0
            scheduler.epoch += 1

            if scheduler.epoch == scheduler.epochs - 1:

                print(f'Time elapsed: {(scheduler.time):.4f}')

                visualizer.visualize(scheduler.grid)
                return
            asyncio.create_task(assign_tasks_to_workers())

    async def assign_tasks_to_workers():
        for i, id in enumerate(scheduler.workers.keys()):
            websocket, assigned_region = scheduler.workers[id]
            payload = scheduler.gen_task_payload(assigned_region)
            await send(websocket, 'task_assign', **payload)


    async def register(websocket, payload):
        name,id = payload['name'], payload['id']

        if name == 'worker':
            scheduler.register_worker(websocket, id)
            print(f'Worker {id}: Registered')

            # broadcast tasks to workers once workers are registered
            if len(scheduler.workers) == scheduler.n_regions and scheduler.status == 0:
                scheduler.time = time.perf_counter()
                scheduler.assign_regions_to_workers()
                asyncio.create_task(assign_tasks_to_workers())
                print('assigned tasks')

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
    s = Scheduler()
    asyncio.run(server())


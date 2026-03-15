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
        region = payload['region']
        region_vals = np.array(payload['region_vals'], dtype='float32')

        # INSTEAD OF SENDING UPDATES WHEN ALL WORKERS ARE DONE
        #   CHECK IF THE WORKERS BOUNDARIES ARE PRESENT
        #       IF WORKERS BOUNDARIES ARE UPDATED THEN UPDATE REGION BOUNDARIES AND GRID AND SEND NEIGHBOR BOUNDARIES BACK
        #       ELSE JUST UPDATE REGION BOUNDARIES AND CONTINUE LISTENING
        scheduler.update_grid(region, region_vals)
        assign_tasks_to_workers()
        if scheduler.n_worker_updates == scheduler.n_regions:
            print(f'Epoch {scheduler.epoch + 1} Complete')
            scheduler.n_worker_updates = 0
            scheduler.epoch += 1
            scheduler.updated_boundaries[:][:] = False

            if scheduler.epoch == scheduler.epochs - 1:

                print(f'Time elapsed: {(scheduler.time):.4f}')

                visualizer.visualize(scheduler.grid)
                return

            asyncio.create_task(assign_tasks_to_workers())

    async def assign_tasks_to_workers():
        updated_boundaries = set(np.where(scheduler.updated_boundaries))
        for i, id in enumerate(scheduler.workers.keys()):
            websocket, assigned_region, adjacent_regions = scheduler.workers[id]
            updated_adj_count = 0
            for r,c in adjacent_regions:
                if (r,c) in updated_boundaries:
                    updated_adj_count += 1
                if r < 0 or r > len(scheduler.n_grid_rows - 1) or c < 0 or c > len(scheduler.n_grid_cols - 1):
                    updated_adj_count += 1
            if updated_adj_count == 4:
                payload = scheduler.gen_task_payload(assigned_region)
                await send(websocket, 'task_assign', **payload)
                scheduler.n_worker_updates += 1



    async def register(websocket, payload):
        name,id = payload['name'], payload['id']

        if name == 'worker':
            scheduler.register_worker(websocket, id)
            print(f'Worker {id}: Registered')

            # broadcast tasks to workers once all required workers are registered
            if len(scheduler.workers) == scheduler.n_regions:
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


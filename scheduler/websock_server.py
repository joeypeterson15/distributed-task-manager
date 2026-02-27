import websockets
import asyncio
from websockets.asyncio.server import serve
from scheduler_class import Scheduler
import json

# {
#     sim_duration: seconds
#     time interval: seconds
#     grid_dim: N X N => (workers = N)
#     region_dim: how many cells occupy each grid(for a 3 X 3 grid, region dim could be 4 x 4 inside each region)
#     initial conditions: List[List => what sections(0 -> N, 0 -> N) of the grid have heat in them] => 

# }

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

            # broadcast tasks to workers once workers are registered
            if len(scheduler.workers) == scheduler.n_regions and scheduler.status == 0:
                print('n workers: ', (len(scheduler.workers)))
                print('n regions:', scheduler.n_regions)
                await assign_tasks()
                scheduler.update_status(1)
            print('assigned tasks')
            
            # wait for worker updates => reassign tasks when all workers done
            while scheduler.status == 1:
                print('in scheduler task assign while loop')
                epoch = 0
                while epoch < scheduler.epochs:
                    n_worker_updates = 0
                    while n_worker_updates < scheduler.n_regions:
                    # update global grid
                        message = json.loads(await websocket.recv())
                        
                        region_coords = message['payload']['region_coords']
                        new_region = message['payload']['region']
                        scheduler.update_grid(region_coords, new_region, epoch)
                        n_worker_updates += 1
                    
                    await assign_tasks(epoch)
                    epoch += 1
                
                scheduler.update_status(2)
            print('result: ', scheduler.grid[3])
            
            # SEND RESULTS TO CLIENT



                    
    async def assign_tasks(epoch=0):
        for i, region_coord in enumerate(scheduler.region_coords):
            payload = scheduler.gen_task_payload(region_coord, epoch)
            await send(scheduler.workers[i], 'task_assign', **payload)


    async def register(websocket, payload):
        name,id = payload['name'], payload['id']

        if name == 'worker':
            scheduler.register_worker(websocket)
            print(f'Worker {id}: Registered')

        if name == 'client':
            tasks = payload['tasks']
            scheduler.register_client(websocket)
            await websocket.send(f'Client Registered')
            scheduler.configure_tasks(tasks)
            await websocket.send(f'Tasks Registered')
         
    async def send(websocket, type, **kwargs):
        message = MESSAGE[type]
        if kwargs: message['payload'] = kwargs
        await websocket.send(json.dumps(message))

    async def main():
        async with serve(handler, "", 8001) as server:
            await server.serve_forever()
    
    await main()

if __name__ == "__main__":
    s = Scheduler()
    asyncio.run(server())


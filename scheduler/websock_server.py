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

            if type == 'stdout':
                print(f'{payload['message']}')

            # broadcast tasks to workers once all workers are registered
            if len(scheduler.workers) == scheduler.n_grid_cols * scheduler.n_grid_rows and scheduler.status == 0:
                await assign_tasks()
                scheduler.update_status(1)
            
            # wait for worker updates, then reassign tasks when all workers done
            while scheduler.status == 1:
                while scheduler.curr_epoch < scheduler.epochs:
                    n_worker_updates = 0
                    while n_worker_updates < scheduler.n_regions:
                    # workers will send updated regions here.
                    #  payload:
                        # worker region
                        # region updated values
                    # scheduler needs to update global grid, and send back new boundary conditions
                        message = json.loads(await websocket.recv())
                        
                        status = message['payload']['status']
                        reg_row, reg_col = message['payload']['region']
                        reg_updates = message['payload']['region_updates'] #needs to be a precision grid => 5 x 5 matrix
                        for m in range(scheduler.n_grid_rows):
                            for n in range(scheduler.n_grid_cols):
                                scheduler.epochs_grid[scheduler.curr_epoch][reg_row][reg_col][m][n] = reg_updates[m][n]

                        n_worker_updates += 1
                    
                    assign_tasks()
                    scheduler.curr_epoch += 1


                    
    async def assign_tasks():
        for i, reg in enumerate(scheduler.regions):
            payload = scheduler.gen_task_payload(reg)
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


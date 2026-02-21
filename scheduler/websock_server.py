import websockets
import asyncio
from websockets.asyncio.server import serve
from scheduler_class import Scheduler

async def server():
    scheduler = Scheduler()

    async def handler(websocket):
        # scheduler = kwargs['scheduler']
        while True:
            worker_id = await websocket.recv()
            print(worker_id)
            scheduler.register(int(worker_id))

            await websocket.send('Message Recieved!')


    async def main():
        async with serve(handler, "", 8001) as server:
            await server.serve_forever()
    
    await main()



if __name__ == "__main__":
    s = Scheduler()
    asyncio.run(server())


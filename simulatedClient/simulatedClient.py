
import websockets
import asyncio
import json
import random
import time
import uuid

connection = websockets.connect(uri='ws://localhost:8765', ping_interval=None)

MSG_TYPE = {
    "REGISTER": 1,
    "REQUEST": 2,
    "RESPONSE": 3
}

JOB_TYPES = [
    "bubbleSort",
    "mergeSort",
    "radixSort"
]

USERS = [
    "user1",
    "user2",
    "user3",
    "user4",
    "user5",
]

IS_REGISTERED = False

async def sendRandomJob(websocket):
    '''
        Send a random job from a random user to the jobHandler.
    '''
    asp_uid = str(uuid.uuid4())
    
    await websocket.send(json.dumps({
        "code": MSG_TYPE["REQUEST"],
        "worker": True,
        "type": JOB_TYPES[random.randint(0, len(JOB_TYPES) - 1)],
        "user": USERS[random.randint(0, len(USERS) - 1)],
        "data": random.sample(range(6, 101), random.randint(5,15)),
        "asp_uid": asp_uid
    }))

async def registerClient(websocket):
    '''
        Register the client.
    '''
    asp_uid = str(uuid.uuid4())
    await websocket.send(json.dumps({
        "code": MSG_TYPE["REGISTER"],
        "client": True,
        "asp_uid": asp_uid
    }))

async def main():
    '''
        Main loop receives jobs, executes them and responds.
    '''
    async with connection as websocket:
        await registerClient(websocket=websocket)
        time.sleep(2)
        try:
            async for message in websocket:
                await sendRandomJob(websocket= websocket)
                time.sleep(random.randrange(1, 10))
        except KeyboardInterrupt:
            print('interrupted!')
        except:
            pass

        await websocket.close()


if __name__ == "__main__":
    asyncio.run(main())
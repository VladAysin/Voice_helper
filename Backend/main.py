from ASR.ASR import SpeechToText, getResult, getResultCommand
import websockets
import asyncio
import time
from threading import Thread

Record = SpeechToText()
Record.start()

class Connect():
    def __init__(self):
        self.connected = set()
        self.data = ''
        self.stopFlag = False

    async def handler(self, websocket, path):
        self.connected.add(websocket)
        try:
            print('OK')
            name = await websocket.recv()
            greeting = f"{name}!"
            await websocket.send(greeting)
            print(f"> {greeting}")

            sendData = asyncio.ensure_future(self.sendData(websocket, path))

            getData = asyncio.ensure_future(self.getData(websocket, path))

            done, pending = await asyncio.wait([sendData, getData],return_when=asyncio.FIRST_COMPLETED,)

            for task in pending:
                task.cancel()
        except:
            print('error')

    async def sendData(self, websocket, path):
        while True:
            try:
                data = getResult()
                result = getResultCommand()
                if data[0] and data[1] != '':
                    await websocket.send('{text:' + data[1]+'}')
                elif result[0]:
                    await websocket.send('{text:' + result[1]+'}')
                time.sleep(0.1)
            except:
                print("Connnect error")
    
    async def getData(self, websocket, path):
        while True:
            coro = await websocket.recv()



sock = Connect()
try:
    print('Connect')
    ws_server = websockets.serve(sock.handler, "10.11.17.2", 22150)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ws_server)
    loop.run_forever()
except KeyboardInterrupt:
    stopFlag = True
    #TODO: close ws server and loop correctely
    print("Exiting program...")



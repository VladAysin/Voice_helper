from ASR.ASR import SpeechToText, getResult, getResultCommand
import websockets
import asyncio
import time
import json
from threading import Thread


Record = SpeechToText()
Record.start()

async def sendData(websocket):
    try:
        while True:
            data = getResultCommand()
            result = getResult()
            if data[0] and data[1] != '':
                print('Send data:  ' + ' '.join(data[1]))
                await websocket.send(json.dumps(
                    {'result': str(' '.join(data[1]))}, 
                    ensure_ascii=False
                    ))
            elif result[0]:
                print('Sennd result: ', result[1])
                await websocket.send(json.dumps(
                    {'result': result[1]}, 
                    ensure_ascii=False
                    ))
            await asyncio.sleep(1)
    except:
        print("Connnect error")
    finally:
        return asyncio.FIRST_COMPLETED

async def getData(websocket):
    try:
        while True:
            coro = await websocket.recv()
            print(coro)
    finally:
        return asyncio.FIRST_COMPLETED

async def handler(websocket, path):
    print('Connect')
    send = asyncio.ensure_future(sendData(websocket))
    get = asyncio.ensure_future(getData(websocket))
    done, pending = await asyncio.wait([send, get],return_when=asyncio.FIRST_COMPLETED,)
    for task in pending:
        task.cancel()

try:
    ws_server = websockets.serve(handler, "10.11.17.2", 22100)
    asyncio.get_event_loop().run_until_complete(ws_server)
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    Record.stopFlag = True
    #TODO: close ws server and loop correctely
    print("Exiting program...")



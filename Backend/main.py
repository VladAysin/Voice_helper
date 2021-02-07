from ASR.ASR import SpeechToText, getResult, getResultCommand, setCommand
import websockets
import asyncio
import time
import json
from threading import Thread



Record = SpeechToText()
Record.start()
#setCommand('в документе для моделирования реактора')



while True:
        data = getResultCommand()
        result = getResult()
        if data[0] and data[1] != '':
            print('Send data:  ' + ' '.join(data[1]))
        elif result[0]:
            print('Sennd result: ', result[1])
        time.sleep(0.1)

# async def sendData(websocket):

#     while True:
#         await websocket.send(json.dumps(
#                 {'text': 'BIBA'}, 
#                 ensure_ascii=False
#                 ))
#         data = getResultCommand()
#         result = getResult()
#         if data[0] and data[1] != '':
#             print('Send data:  ' + ' '.join(data[1]))
#             await websocket.send(json.dumps(
#                 {'text': str(' '.join(data[1]))}, 
#                 ensure_ascii=False
#                 ))
#         elif result[0]:
#             print('Sennd result: ', result[1])
#             await websocket.send(json.dumps(
#                 {'result': json.dumps(result[1])}, 
#                 ensure_ascii=False
#                 ))
#         await asyncio.sleep(3)
   

# async def getData(websocket):

#     while True:
#         coro = await websocket.recv()
#         print(coro)
#         setCommand(coro)


# async def handler(websocket, path):
#     print('Connect')
#     send = asyncio.ensure_future(sendData(websocket))
#     get = asyncio.ensure_future(getData(websocket))
#     done, pending = await asyncio.wait([send, get],return_when=asyncio.FIRST_COMPLETED,)
#     for task in pending:
#         task.cancel()

# try:
#     ws_server = websockets.serve(handler, "10.11.17.2", 1337)
#     asyncio.get_event_loop().run_until_complete(ws_server)
#     asyncio.get_event_loop().run_forever()
# except KeyboardInterrupt:
#     Record.stopFlag = True
#     #TODO: close ws server and loop correctely
#     print("Exiting program...")



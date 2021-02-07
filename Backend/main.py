from ASR.ASR import SpeechToText, getResult, getResultCommand, setCommand, SpeechToTextButton
import websockets
import asyncio
import time
import json
from threading import Thread



Record = SpeechToText()
#Record.start()
Record.stopFlag = True
Record.END = True
#setCommand('в документе для моделирования реактора')
Test = SpeechToTextButton()

class WaitRecord(Thread):
    def __init__(self):
        Thread.__init__(self) 
    def run(self):
        while not(Record.END):
            time.sleep(0.5)
        Test.start()
        while Test.result == '':
            time.sleep(0.5)
        print(setCommand(Test.result))

wait = WaitRecord()
wait.start()

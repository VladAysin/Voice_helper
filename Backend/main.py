from ASR.ASR import SpeechToText, getResult, getResultCommand, setCommand, SpeechToTextButton
# import websockets
# import asyncio
import time
import json
from threading import Thread



Record = SpeechToText()
#Record.start()
Record.stopFlag = True
Record.END = True
#setCommand('в документе для моделирования реактора')
Test = SpeechToTextButton()



wait = WaitRecord()
wait.start()

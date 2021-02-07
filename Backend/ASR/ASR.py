from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_silence
import pyaudio
import wave

import requests
import ast
from threading import Thread
from random import randrange
import os
import time
from commands.command import *

import configparser

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("config.ini")

ROMA = False
RESULT = ''
DATA = []
#DATASEND = []
OK = [False, 0]

class MyTimer(Thread):
    '''
    Custom Timer class for len of speech command
    '''
    def __init__(self):
        Thread.__init__(self) 
    def run(self):
        global ROMA
        time.sleep(5)
        #print('END')
        ROMA = False

mytimer = MyTimer()


def goCommand(text):
    global RESULT
    print('command: ', text)
    RESULT = run_command(text, config)
    print(RESULT)

def setCommand(text):
    print('command: ', text)
    RESULT = run_command(text, config)
    ROMA = True
    OK = [True, 0]
    return RESULT

def createCommand(text):
    global ROMA
    global OK
    global DATA

    if OK[1] >= 1 and DATA != []:
        ROMA = False
        goCommand(' '.join(DATA))
        DATA = []
        OK[1] = 0
    if text != '':
        DATA.append(text)
        #DATASEND.append(text)
        OK[0] = True
    else:
        OK[1] +=1

def getResult():
    global RESULT
    r = RESULT
    if r:
        RESULT = ''
        print(r)
        return [True, r]
    return [False, '']

def getResultCommand():
    global OK
    #global DATASEND
    #data = DATASEND.copy
    #DATASEND = []
    if OK[0]:
        OK[0] = False
        return [True, DATA]
    return [False, '']


class Recognition(Thread):
    '''
    Class in same thread for send audio frame to our ASR
    '''
    def __init__(self,name,url,asr):
        Thread.__init__(self)
        self.name = name
        self.text = ''
        self.url = url
        self.asr = asr
    def run(self):
        global ROMA
        #print(self.url)
        wav = open(self.url, 'rb')
        multiple_files = [('audio_blob', (self.url, wav, 'sound/wav'))]
        try:
            r = requests.post("http://10.11.17.6:8888/asr", files=multiple_files)
        except Exception as err:
            print('error: ', err)
        wav.close()
        os.remove(self.url) 
        try:
            result = ast.literal_eval(r.text)['r'][0]['response'][0]['text']
            if 'рома' in result and not(ROMA):
                ROMA = True
                mytimer.start()
            if ROMA:
                print(result)
                createCommand(result)
            print('F ===============',result)
        except:
            pass
            #print('error: {r}')
        #self.text = ast.literal_eval(r.text)['r'][0]['response'][0]['text']
class SpeechToText(Thread):
    '''
    Speech To Text function by Rusil

    Funct start():
    Start while true listen, segmentation and recognition stream from mic.

    Record for 500ms;
    Rate sound 44100 Hz;
    Chunk size 1024 (2048 bytes);
    Channel 1;
    int 16 bit;
    '''
    def __init__(self,):
        Thread.__init__(self)
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.RECORD_SECONDS = 0.5

        self.silence_thresh=-38
        self.min_silence_len=100

        self.url_asr = config['ASR']['url']
        self.ok = False
        self.stopFlag = False

        self.END = False

    def run(self):
        global ROMA
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = 0.5
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

        print("Recording...")
        frames = []
        ok = 0
        split = 0
        while not(self.stopFlag):

            for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

            sound_file = AudioSegment(
                b''.join(frames),
                sample_width=2, 
                channels=1,
                frame_rate=RATE
            )
            audio_chunks = detect_silence(sound_file, 
                min_silence_len=self.min_silence_len,
                seek_step=1,
                silence_thresh=self.silence_thresh
            )
            #print(len(frames),audio_chunks)
            if len(audio_chunks) != 0 or split:
                if (audio_chunks[0][1] < 488 and len(audio_chunks) == 1):
                    continue
                if (audio_chunks[0][1] < 488 and len(audio_chunks) >= 2) or ok:
                    url = 'ASR/audio/'+str(randrange(64000))+'.wav'

                    wf = wave.open(url, 'wb')
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(p.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(frames))
                    wf.close()

                    r = Recognition('f',url, asr = self.url_asr)
                    r.start()

                    frames = []
                    ok = 0
                    continue
                if (audio_chunks[0][0] > 50 and len(audio_chunks) >=2 ) or ok:
                    url = 'ASR/audio/'+str(randrange(64000))+'.wav'

                    last_frame.extend(frames)

                    wf = wave.open(url, 'wb')
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(p.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(last_frame))
                    wf.close()

                    r = Recognition('f',url, asr = self.url_asr)
                    r.start()

                    frames = []
                    last_frame = []
                    ok = 0
                    continue
                
                last_frame = frames
                frames = []
                ok = 0
            else:
                if len(frames) < 2000:
                    ok = 1
                    split = 0
                else:
                    ok = 0
                    split = 1
        stream.stop_stream()
        stream.close()
        p.terminate()
        self.END = True

class SpeechToTextButton(Thread):
    def __init__(self):
        Thread.__init__(self) 
        self.result = ''
    def run(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = 4
        p = pyaudio.PyAudio()

        print("Recording...")
        stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

        #print("sleep...")
        frames = []
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        url = 'ASR/audio/'+str(randrange(64000))+'.wav'

        wf = wave.open(url, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


        wav = open(url, 'rb')
        multiple_files = [('audio_blob', (url, wav, 'sound/wav'))]
        try:
            r = requests.post("http://10.11.17.6:8888/asr", files=multiple_files)
            
        except Exception as err:
            print('error: ', err)
        wav.close()
        os.remove(url) 
        try:
            self.result = ast.literal_eval(r.text)['r'][0]['response'][0]['text']
        except Exception as err:
            self.result = 'Error'
            print('error: ',err)
        r.close()
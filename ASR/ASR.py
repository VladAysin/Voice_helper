from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_silence
import pyaudio
import wave

import requests
import ast
from threading import Thread
from random import randrange
import os
import datetime
import time

WAVE_OUTPUT_FILENAME = "ASR/audio/words.wav"
ROMA = False
def goCommand(text):
    print(text)


class MyTimer(Thread):
    def __init__(self):
        Thread.__init__(self) 
    def run(self):
        global ROMA
        time.sleep(20)
        #print('END')
        ROMA = False

class Recognition(Thread):
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
        r = requests.post(self.asr, files=multiple_files)
        wav.close()
        os.remove(self.url) 
        try:
            result = ast.literal_eval(r.text)['r'][0]['response'][0]['text']
            if 'рома' in result and not(ROMA):
                ROMA = True
                t=MyTimer()
                t.start()
                #print('start')
            if ROMA:
                goCommand(result)
            #print('F _____',result)
        except:
            pass
            #print(r.text)
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
    def __init__(self, urlASR = 'http://10.11.17.13:8888/asr'):
        Thread.__init__(self)
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.RECORD_SECONDS = 0.5

        self.silence_thresh=-52
        self.min_silence_len=100

        self.url_asr = urlASR

        self.Timer = 0
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
        while True:

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
            if len(audio_chunks) != 0:
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
                ok = 1

        stream.stop_stream()
        stream.close()
        p.terminate()

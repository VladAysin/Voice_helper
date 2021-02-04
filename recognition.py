import requests
import json
import ast

def recognition():
    multiple_files = [('audio_blob', ('output.wav', open('sound/output.wav', 'rb'), 'sound/wav'))]
    r = requests.post('http://10.11.17.13:8888/asr', files=multiple_files)
    return ast.literal_eval(r.text)['r'][0]['response'][0]['text']
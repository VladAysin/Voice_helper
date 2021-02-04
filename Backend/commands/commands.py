import json 
import os

print(os.getcwd())

with open("./commands/command.json","r",encoding="utf-8") as f:
    command = json.load(f)

print(command)
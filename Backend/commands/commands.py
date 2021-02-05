import json
import os
from scripts.script import *

with open(
    os.path.dirname(os.path.abspath(__file__)) + 
    "\command.json", "r", 
    encoding="utf-8") as f:
    commands = json.load(f)


def run_command(command):
    try:
        command = command.split(" ")
        if len(command) < 3:
            exec(commands[command[0]][command[1]]+"()")
    except:
        return {"type": "text", "data": "Команда не может быть выполнена"}

run_command("покажи погоду")
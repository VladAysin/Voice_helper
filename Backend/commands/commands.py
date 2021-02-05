import json
import os
from Backend.commands.scripts.script import *

with open("./command.json", "r", encoding="utf-8") as f:
    commands = json.load(f)


def run_command(command, **kwargs):
    try:
        command = command.split(" ")
        if len(command) < 3:
            exec(commands[command[0]][command[1]]["command"]+"()")
    except:
        return {"type": "text", "data": "Команда не может быть выполнена"}

run_command("покажи погоду")
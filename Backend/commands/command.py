import json
import os
import pymorphy2
from scripts.script import *
morph = pymorphy2.MorphAnalyzer()

with open(
    os.path.dirname(os.path.abspath(__file__)) + 
    "\commands.json", "r", 
    encoding="utf-8") as f:
    commands = json.load(f)


def run_command(command):

    def lemmatizing(command):
        lemma_command = []
        for word in command:
            lemma_word = morph.parse(word)[0].normal_form
            lemma_command.append(lemma_word)
        return lemma_command

    def find_command(our_command,commands):
        while True:
            
            if type(commands) == str:
                break
            else:
                words = [word for word in commands]
                lemma_words = lemmatizing(commands)
                for word in lemma_words:
                    if word in our_command:
                        commands = commands[words[lemma_words.index(word)]]

                commands = list(commands.values())[0]
        return commands

    global commands

    command = lemmatizing(command.split(" "))
    command = find_command(command,commands)
    try:
        exec(command+'()')
    except:
        return {"type": "text", "data": "Команда не может быть выполнена"}

run_command("покажи погоду")
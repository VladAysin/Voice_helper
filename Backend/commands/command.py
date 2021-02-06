import json
import os
import types
import pymorphy2
from .commands import *
morph = pymorphy2.MorphAnalyzer()

commands = dict_commands

<<<<<<< HEAD

def run_command(command, config):
=======
def run_command(command):
>>>>>>> 501c02e908ac9c3de3b2e81ca22df0e17f269cfe

    def lemmatizing(command):
        lemma_command = []
        for word in command:
            lemma_word = morph.parse(word)[0].normal_form
            lemma_command.append(lemma_word)
        return lemma_command

    def find_command(our_command,commands):
        while True:
            
            if type(commands) == types.FunctionType:
                break
            else:
                
                words = [word for word in commands]
                lemma_words = lemmatizing(commands)
                for word in lemma_words:
                    if word in our_command:
                        commands = commands[words[lemma_words.index(word)]]
                        our_command.remove(word)

        return commands

    global commands
    command = lemmatizing(command.split(" "))
    analysis = ["оборудование","состояние"]
    for word in lemmatizing(analysis):
        if word in command:
            return xls_analysis(command)

    command = find_command(command,commands)
    try:
        return command() 
    except:
        return {"type": "text", "data": "Команда не может быть выполнена"}

run_command("покажи список оборудования")
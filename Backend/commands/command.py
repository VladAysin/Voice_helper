import json
import os
import types
import pymorphy2
from .commands import *
morph = pymorphy2.MorphAnalyzer()

commands = dict_commands

def run_command(command, config):

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
    file_found = ['файл']
    for word in lemmatizing(file_found):
        if word in command:
            return find_file_on_fs('flag.txt')
    command = find_command(command,commands)
    try:
        return command() 
    except:
        return {"type": "text", "data": "Команда не может быть выполнена"}
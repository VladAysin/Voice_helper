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
        copy_command = our_command.copy()
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
                if len(our_command) == len(copy_command):
                    break
        return commands
    global commands

    pdffind = ['в', 'документе']
    for word in lemmatizing(pdffind):
        some_command = lemmatizing(command.split(' '))
        if word in some_command:
            return findInPDF(" ".join(command.split(" ")[2:]),'./')
        # cum = ' '.join(command)
        # com = cum.replace(' '.join(pdffind),'')
        

    command = lemmatizing(command.split(" "))
    analysis = ["оборудование","состояние"]
    for word in lemmatizing(analysis):
        if word in command:
            return xls_analysis(command)

    file_found = ['файл']
    for word in lemmatizing(file_found):
        if word in command:
            return find_file_on_fs('письма')

    try:
        command = find_command(command,commands)
        return command() 
    except:
        return "Команда не может быть выполнена"
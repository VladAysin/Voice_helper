from threading import Thread
from queue import Queue
import win32api
import os
import pandas as pd
import numpy as np
import sys
import traceback
status = ['работа','дефект','наряд','резерв']
queue = Queue()

class Find_file(Thread):
    def __init__(self,drive,file_name):
        Thread.__init__(self)
        self.drive = drive
        self.file_name = file_name
        self.list_dirs = []
        self.result = ''

    def run(self):
        self.list_dirs = list(os.walk(self.drive))
        for info in self.list_dirs:
            if self.file_name in info[-1]:
                self.result = info[0]+ "\\" + self.file_name
        queue.task_done()


def helloworld(a, b):
    print("hello world", a, b)


def startbrowser():
    os.system("start www.google.com")
    return 0

def weather():
    from requests import  get
    try:
        r = get("http://ipinfo.io").json()
        city = r["city"]
        key = "b5db848c6f1317ccddf157a8c3d8112e"
        r = get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={key}&lang=ru").json()
        answer = r["main"]
        answer.update(r["weather"][0])
        print(answer)
        return answer
    except Exception as err:
        e = sys.exc_info()[2]
        tbinfo = traceback.format_tb(e)[0]
        print(err,"\n",tbinfo,)
        return 1

def launchProgramm(program:str):
    programs = {
        "explorer":["проводник","мой компьютер","explorer"],
        "browser":["браузер","сайт росатома"]
    }
    try:
        if program in programs["explorer"] :
            program = "explorer"
        elif program in programs["browser"] :
            program = "https://rosatom.ru/"
        os.system(f"start {program}")
        return 0
    except Exception as err:
        e = sys.exc_info()[2]
        tbinfo = traceback.format_tb(e)[0]
        print(err,"\n",tbinfo,)
        return 1

def xls_analysis(command):
    global status
    dict_all = {}
    try:
        for info in os.walk('./folder'):
            for xls_name in info[-1]:
                try:
                    xls = pd.read_html(info[0]+'/'+xls_name)
                    df = pd.DataFrame(xls[0])
                    df.columns = df.loc[0,:].to_list()
                    df = df.loc[1:,:].reset_index(drop=True)
                    df['Состояние'] = pd.Series()
                    df['Состояние'] = np.random.choice(status,len(df))
                    if 'список' in command:
                        dict_spisok = {'Столбцы':['Описание',"Состояние"]}
                        desc = df['Описание'].to_dict()
                        status = df['Состояние'].to_dict()
                        for i in desc:
                            dict_spisok.update({i:[desc[i],status[i]]})
                    dict_all.update({info[0]+'/'+xls_name:dict_spisok})
                except Exception as err:
                    e = sys.exc_info()[2]
                    tbinfo = traceback.format_tb(e)[0]
                    print(err,"\n",tbinfo,)
                    continue
        return dict_all
    except Exception as err:
        e = sys.exc_info()[2]
        tbinfo = traceback.format_tb(e)[0]
        print(err,"\n",tbinfo,)
        return 1


def find_file_on_fs(file_name,path=''):
    if path == '':
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1] 
    else:
        drives = [path]
    dict_drives = {}
    
    for path in drives:
        dict_drives.update({path:Find_file(path,file_name)})
        queue.put(dict_drives[path].start())
    queue.join()

    list_files = []
    for path in drives:
        list_files.append(dict_drives[path].result)
    dict_files = {file_name:list_files}

    return dict_files


def readPDF(path:str):
    try:
        if path.lower().endswith(".pdf"):
            pass

        else:
            return 1
    
    except Exception as err:
        e = sys.exc_info()[2]
        tbinfo = traceback.format_tb(e)[0]
        print(err,"\n",tbinfo,)
        return 1


if __name__ == "__main__":
    weather()
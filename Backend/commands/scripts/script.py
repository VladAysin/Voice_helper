import os
import pandas as pd
import numpy as np
import sys
import traceback
from cleantext import clean
import pdfplumber
import glob
import re
from threading import Thread
from queue import Queue
status = ['работа','дефект','наряд','резерв']



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

def readPDF(path:str):
    try:
        if path.lower().endswith(".pdf"):
            with pdfplumber.open(path) as pdf:
                if (len(pdf.pages)):
                    text = " ".join([
                        page.extract_text() or " " for page in pdf.pages if page
                    ])
            clear_text = clean(text, lang='ru', lower=False, to_ascii=False)
            return clear_text

        else:
            return 1
    
    except Exception as err:
        e = sys.exc_info()[2]
        tbinfo = traceback.format_tb(e)[0]
        print(err,"\n",tbinfo,)
        return 1

    
def findInPDF(text,path):


    class FindInPDF(Thread):
        def __init__(self,path,text,result):
            super(FindInPDF,self).__init__()
            self.path = path
            self.text = text
            self.result = result

        def run(self):
            text1 = readPDF(file)
            if re.findall(text,text1,flags=re.IGNORECASE):
                self.result.append(file)
            q.task_done()


    try:

   
        files = [
            glob.glob(os.path.join(folder[0],"*.pdf"))
            for folder in os.walk(path)
            if glob.glob(os.path.join(folder[0],"*.pdf"))
        ][0]
        result = []
        q = Queue()
        for file in files:
            thread = FindInPDF(path,text,result)
            q.put(thread.start())
        
        q.join()
        if result:
            print(result)      
    except Exception as err:
        e = sys.exc_info()[2]
        tbinfo = traceback.format_tb(e)[0]
        print(err,"\n",tbinfo,)
        return 1  

    


if __name__ == "__main__":
    # readPDF("D:\\project\\Voice_helper\\Backend\\HackAtom_Data\\pdf_material\\01.pdf")
    findInPDF("вплоть до полного разрушения","D:\\project\\Voice_helper\\Backend\\HackAtom_Data\\")


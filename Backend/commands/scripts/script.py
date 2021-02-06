import os
import pandas as pd
import numpy as np
import sys
import traceback
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
                    print("Error",err)
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
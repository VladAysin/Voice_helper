import os


def helloworld(a, b):
    print("hello world", a, b)


def startbrowser():
    os.system("start www.google.com")

def weather():
    from requests import  get
    r = get("http://ipinfo.io").json()
    city = r["city"]
    key = "b5db848c6f1317ccddf157a8c3d8112e"
    r = get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={key}&lang=ru").json()
    answer = r["main"]
    answer.update(r["weather"][0])
    print(answer)
    return answer

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
    except Exception as err:
        print("Error",err)
    return None

            


if __name__ == "__main__":
    launchProgramm("браузер")
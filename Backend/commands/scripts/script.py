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
    print("requests\n",answer)
    print('something')

import os

def search(words,dictionary):
    for word in words:
        for i in dictionary:
            if i in word:
                return True
    return False

def command(text):
    words_and = str.split(text,' и ')
    AND = len(words_and) == 2
    if AND:
        words = str.split(words_and[0],' ')
        words_and1 = str.split(words_and[1],' ')
    else:
        words = str.split(text,' ')

    # Запуск браузера
    action = ['пусти','включи','выпол','откр','отро','включ','запус','выпуст']
    subject = ['браузе','яндекс','бауз','баусе','браусе','янде']
    if search(words, action) & search(words, subject):
        if AND:
            print(words_and1)
            action = ['найд','отыщ','вед','найт']
            if search(words_and1, action):
                words_and1.pop(0)
                find = "%20".join(words_and1)
                os.system(r'start https://yandex.ru/search/?text=' + find)
                return
        os.startfile(r'C:\\Users\\Rusil\\AppData\\Local\\Yandex\\YandexBrowser\\Application\\browser.exe')
        return
    
    
    # Поиск в браузере
    action = ['найд','отыщ','вед','найт','покаж','пока','поко','откр']
    if search(words, action):
        words.pop(0)
        find = "%20".join(words)
        os.system(r'start https://yandex.ru/search/?text=' + find)
        return
    
    # Запуск командной строки
    action = ['опусти','включи','выпол','откр','отро','включ','запус']
    subject1 = ['командную','коман']
    subject2 = ['строк']
    if search(words, action) & search(words, subject1) & search(words, subject2):
        os.startfile(r'C:\\Windows\\system32\\cmd.exe')
        return
    


    action = ['найд','отыщ','вед','найт']
    if search(words, action):
        os.system(r'start https://yandex.ru/search/?text=' + words[1:])
        return
    
    action = ['иди','пошел','пошёл']
    subject1 = ['нах','хуй']
    if search(words, action) & search(words, subject1):
        os.system(r'start https://yandex.ru/search/?text=сам%20иди%20нахуй')
        return
    
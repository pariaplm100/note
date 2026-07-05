from random import randint 

def Captcha():
    text = ""

    for i in range(0,5):
        text += str(randint(0, 9))

    return int(text)
    
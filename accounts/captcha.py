from random import randint 

def Captcha():
    text = ""

    for i in range(0,2):
        text += str(randint(1, 9)) 
        
    for j in range(0,1):
        text += str(chr(randint(65,90)))
        
    for i in range(0,1):
        text += str(randint(1, 9))   
         
    for j in range(0,1):
        text += str(chr(randint(97,122)))
                
    return text
    

from random import randint

otp = randint(100000, 999999)
request.session["otp"] = str(otp)
import os

def pickcomputer(): #when changing which computer I'm using
    global directory
    if os.path.exists("C:/Users/avboy/Documents/GitHub - Personal"): #laptop
        directory = "C:/Users/avboy/Documents/GitHub - Personal"
    elif os.path.exists("C:/Users/Avery B/"): #pc
        directory = "C:/Users/Avery B/"
    elif os.path.exists("G:/Avery's funny business/Github/"):
        directory = "G:/Avery's funny business/Github/"
    return directory
directory = pickcomputer()
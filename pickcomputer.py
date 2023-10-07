import os

def pickcomputer(): #when changing which computer I'm using
    if os.path.exists("C:/Users/avboy/Documents/GitHub - Personal"): #laptop
        directory = "C:/Users/avboy/Documents/GitHub - Personal"

    elif os.path.exists("C:/Users/Avery B/"): #personal desktop pc
        directory = "C:/Users/Avery B/Documents/My Documents/GitHub"

    elif os.path.exists("G:/Avery's funny business/Github/"): #at home pc
        directory = "G:/Avery's funny business/Github"
    return directory
directory = pickcomputer()

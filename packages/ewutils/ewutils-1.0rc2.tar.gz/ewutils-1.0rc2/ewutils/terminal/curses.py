import os

def hideShell():
    os.system("tput smcup")

def showShell():
    os.system("tput rmcup")

def place(message:str, x:int, y:int):
    print(f"\u001b[{y};{x}H{message}")
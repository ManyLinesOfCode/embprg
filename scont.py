from machine import Pin, PWM
from servo_translator import translate

s1=PWM(Pin(0)) # shoulder
s2=PWM(Pin(1)) # elbow
s3=PWM(Pin(2)) # wrist

def translate(angle:float) -> int:
    MIN=1638
    MAX=8192
    DEG=(MAX-MIN)/180
    angle=max(0,min(180,angle))
    return int(angle*DEG+MIN)
st=translate

def move(servo:PWM,deg:int) -> None:
    servo.duty_u16(st(deg))

def execute(gcodearray:list) -> None:
    n=0 # index number
    for i in gcodearray:
        if i=="M18":
            print("Read stop code.") & SystemExit()
        elif i=="M5":
            move(s3,30) # UP
        elif i=="M3":
            move(s3,-30) # DOWN
        elif i=="G1":
            move(s1,float(gcodearray[n+1][1:])) # pass the element after G1, minus the first character
            move(s2,float(gcodearray[n+2][1:])) # pass the one after that
        elif i[0]=="S" or i[0]=="E": # Ignore degrees themselves
            print("Ignoring.")
        else:
            print(f"Parsing error: Unknown command \"{i}\".")
        n+=1

with open(r"C:\Users\User\Downloads\circle.gcode") as f: # Change this path
    file=f.read()

execute(file.split())

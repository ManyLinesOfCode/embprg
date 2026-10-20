from machine import Pin, RTC
from time import sleep
from matplotlib import pyplot

btn=Pin(12)
rtc=RTC()

def graphlog() -> None:
    with open("log.txt", "r") as file:
        arr=[]
        for i in file.lines(): # numericise
            arr.append(int(i))
        arr.sort()

        pyplot.hist(arr)
        pyplot.show(arr)

print("Press a button, time 15 seconds in your head, then press again and see how close you were.\nThe timer starts upon depression, not release!")
while True:
    if btn.value()==1:
        sleep(0.1) # bounce padding
        start=str(rtc.datetime())[23:-4] # get current second

        log=open("log.txt", "a+") # open logfile

        while True:
            if btn.value()==1:
                # get difference between starting time and now
                stoptime=str(rtc.datetime())[23:-4]
                if stoptime<start: # in the case of minute rollover
                    guess=int(start)-int(stoptime)
                else:
                    guess=int(stoptime)-int(start)

                log.write(str(guess))
                log.close() # close and write

                # communicate with the user
                print(f"Your guess: {guess}")
                if guess>15:
                    print(f"High by {guess-15} seconds.")
                elif guess<15:
                    print(f"Low by {15-guess} seconds.")
                else:
                    print("Right on target!")
                
                break

        print("Press to go again. Timer starts when you do.")
        while True:
            sleep(0.1)
            if btn.value()==1:
                break
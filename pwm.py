from machine import Pin, PWM, ADC
from time import ticks_us, ticks_diff
from array import array

### MEASURE WAVE
def getfeatures(states, nor):
    highs=0 # count the HIGHs
    for i in states:
        if i==1: highs+=1
        
        duty=(highs/nor)*100 # calc duty factor
        avg=3.3*(duty/100)   # calc avg voltage
        print(f"\tMeasured duty factor of {round(duty,2)}%, average of {round(avg,2)}V.")
    del nor

def takereadings(type):
    print("\tTaking readings...",end=" ")

    tstamps=array("I") # Initalise arrays to store readings
    start=ticks_us() # Establish start time to count a second from

    if type=="ac":
        vals=array("B")
        while ticks_diff(ticks_us(),start) < 1_000_000:
            elapsed=ticks_diff(ticks_us(),start)
            vals.append(OUTPIN.value()) # log the state
            tstamps.append(elapsed)     # and elapsed time
    elif type=="dc":
        vals=array("I")
        while ticks_diff(ticks_us(),start) < 1_000_000:
            elapsed=ticks_diff(ticks_us(),start)
            vals.append(adc.read_u16())
            tstamps.append(elapsed)
    else: SystemExit("Error: Desired wave must be AC or DC.")

    # Display number of readings and time spent
    nor=0
    for i in vals: nor+=1
    print(f"Done\n\tTook {nor} readings over {tstamps[-1]}ms.")
    del tstamps

    if type=="ac": getfeatures(vals,nor)
    del nor
    
    return vals

### EMIT WAVE
OUTPINNUM=0 # IMPORTANT: Numbers correspond to GPx signal labels, NOT physical pins!
OUTPIN=Pin(OUTPINNUM)
pwm=PWM(OUTPIN, freq=9, duty_u16=32768) #freq: min 9, max 125_000; duty: min 0, max 65536
print(f"PWM wave being emitted from pin {OUTPINNUM} at {pwm.freq()}Hz...")

### DIGITAL STUFF
print("\nFirst phase:")
states=takereadings(type="ac")

### ANALOG STUFF
print("\nSecond phase:")

ANINPINNUM=26 # TODO: Find the pin that the filter outputs to
ANINPIN=Pin(ANINPINNUM) # GPs 26, 27 and 28 can take analogue input
adc=ADC(ANINPIN)

# Convert analog back to digital
anvals=takereadings(type="dc")
convstates=array("B")
for i in anvals:
    if i<500:
        convstates.append(0)
    elif i>1500:
        convstates.append(1)

nor=0 # Display properties
for i in convstates: nor+=1
getfeatures(convstates, nor)

# TODO: Calculate difference.

### END
pwm.deinit()
print("\nEmission stopped.")
SystemExit()

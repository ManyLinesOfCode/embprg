from machine import Pin, UART

uart=UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
uart.init(bits=8, parity=None, stop=1)


## DECLARE METHODS FOR SENDING AND RECEIVING
def send(string):
    uart.write(b"\x00") # startbyte
    uart.write(string)  # message
    uart.write(b"\xFF") # endbyte
    uart.flush() # off and away

def recv():
    buffer=bytearray()
    while True:
        data=uart.read(1)
        if not data: continue

        byte=data[0]

        if byte==0x00:
            buffer=bytearray()
        elif byte == 0xFF:
            return buffer.decode("utf-8") # The message, stripped of delim bytes, as UTF-8
        else: buffer.append(byte)


## ESTABLISH AND CONFIRM CONNECTION
sender=False
if input("Is this machine the originator? (y/n)")=="y": sender=True

if sender:
    uart.write(b"\x00") # Response should be "Response"
    while True:
        if uart.read(8)==b"\xff":
            print("Connection established.")
            break
else: # if the reader
    while True:
        if uart.read(4)==b"\x00":
            uart.write(b"\xff")
            break


## MAIN LOOP
reclog=[]
while True:
    if sender:
        send(str(input("Say something: ")))
        sender=False
    else: # if receiver
        reclog.append(recv())
        for msg in reclog:
            print(f"{msg}\n\n")
        sender=True


#EXIT
print("Exiting.")
uart.deinit()
SystemExit()

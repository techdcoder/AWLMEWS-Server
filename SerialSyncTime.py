import serial, datetime

arduinoSerial = serial.Serial(port="/dev/ttyUSB0",baudrate=115200)

while True:
    dt = datetime.datetime.now()
    ms = dt.microsecond / 1000
    second = dt.second
    minute = dt.minute
    hour = dt.hour
    if ms < 0.001:
        outStr = f"{hour} {minute} {second}\n"
        print(outStr)
        arduinoSerial.write(outStr.encode())

        break
str = ""
while True:
    ch = arduinoSerial.read().decode()
    if str == '\r':
        continue
    str += ch
    if ch == '\n':
        print(str)
        break
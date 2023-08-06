# This class implements the "driver" object, that allows for communication with a Lin Engineering stepper motor driver.

class driver:

    import serial # PySerial
    import time

    # Constructor
    def __init__(self,portname,address=1):
        self.portname = portname # name of serial port in use
        self.address = str(address) # address of the contoller (default is 1)

        # some default values, from Lin
        self.m = 30 # running current (% max deliverable to motor)
        self.h = 10 # holding current
        self.j = 256 # step resolution
        self.V = 305175 #microsteps / second
        self.L = 1000 # acceleration
        self.o = 1500 # microstep smoothness
        self.b = 9600 # baud rate

        self.tc = '\r' # termination character for command strings

    
    # Set address (make this driver interact with a different physical motor driver)
    def SetAddress(self,address=1):
        self.address = str(address)

    # Run a command
    def RunCommand(self,command_string):
        ser = serial.Serial(self.portname,timeout=0)
        ser.flushInput()
        ser.flushOutput()
        ser.write(bytes(command_string,'utf8'))
        time.sleep(0.1) # avoid closing the serial port mid-command
        ser.close()

    # Create command string
    def MakeCommand(self,input_string):
        return '/'+ self.address + input_string + self.tc

    # Set running parameters
    def SetParams(self,m=self.m,h=self.h,j=self.j,V=self.V,L=self.L,o=self.o,b=self.b):
        self.m = m
        self.h = h
        self.j = j
        self.V = V
        self.L = L
        self.o = o
        self.b = b
        self.RunCommand(MakeCommand(self, 'm' + str(m) + 'h' + str(h) + 'j' + str(j) + 'V' + str(V) + 'L' + str(L) + 'o' + str(o) + 'b' + str(b)))

    # Clear controller memory
    def ClearMemory(self):
        self.RunCommand(MakeCommand(self,'?9'))

    # Step forward/backward x microsteps, x in range x = {0,2^31}
    def Step(self, x, forward = True):
        x = (int(x))%(2**31)

        # if moving backwards, we will reverse polarity.
        # alternatively we can use the Lin "D" command,
        # but this is less reliable as it will not
        # work if we happen to be at position zero.
        if forward == False:
            self.RunCommand(MakeCommand(self,'F1'))

        self.RunCommand(MakeCommand(self,'P'+ str(x)))

        # reverse polarity again if we did it before
        if forward == False:
            self.RunCommand(MakeCommand(self,'F1'))

    # Move to absolute position x, x in range x = {0,2^31}
    def MoveTo(self, x):
        x = (int(x))%(2**31)
        self.RunCommand(MakeCommand(self,'A' + str(x)))

    # Define current position as position x, x in range x = {0,2^31}
    def SetPosition(self,x):
        x = (int(x))%(2**31)
        self.RunCommand(MakeCommand(self,'z' + str(x)))



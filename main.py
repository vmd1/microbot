import microbit
from bluezero import async_tools
from gpiozero import Robot

# Right motor GPIOs
R1=9 # H-Bridge 1
R2=10 # H-Bridge 2
RS=18 # H-Bridge 1,2EN

# Left motor GPIOs
L1=5 # H-Bridge 3
L2=6 # H-Bridge 4
LS=13 # H-Bridge 3,4EN

def cmd (mio):
    mesg=input('cmd: ')
    if mesg == 'forward':
        mio.robot.forward()
    elif mesg =='left':
        mio.robot.left()
    elif mesg == 'right':
        mio.robot.right()
    elif mesg == 'back':
        mio.robot.backward()
    elif mesg == 'stop':
        mio.robot.stop()
class Mio:
    def __init__(self, bluetooth_addr):
        self.bluetooth_addr = bluetooth_addr
        self.eloop = async_tools.EventLoop()
        self.robot = Robot(left=(L1,L2),right=(R1,R2))

    def connectToMicrobit(self):
        self.ubit = microbit.Microbit(device_addr=self.bluetooth_addr,
                         accelerometer_service=False,
                         button_service=False,
                         led_service=False,
                         magnetometer_service=False,
                         pin_service=False,
                         temperature_service=False,
                         uart_service=True)
        self.ubit.connect()
        self.ubit.subscribe_uart(self.onUartMessage)
        self.eloop.add_timer(30000, self.goodbye)
        self.ubit.run_async()

    def goodbye(self):
        self.ubit.quit_async()
        self.ubit.disconnect()
        return False

    def onUartMessage(self, msg):
        print(msg)
        if msg == 'forward':
            self.robot.forward()
        elif msg =='left':
            self.robot.left()
        elif msg == 'right':
            self.robot.right()
        elif msg == 'back':
            self.robot.backward()
        elif msg == 'stop':
            self.robot.stop()
        cmd (mio)


#start here
mio = Mio("D6:38:02:51:F5:83")
mio.connectToMicrobit()
cmd (mio)

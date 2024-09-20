import subprocess
from pynput.keyboard import Key, Controller
import time
import psutil

# Function to get battery information
def OSHandler(query):
	if isContain(query, ['system', 'info']):
		return ['Here is your System Information...', '\n'.join(systemInfo())]
	elif isContain(query, ['cpu', 'battery']):
		return batteryInfo()
    
def batteryInfo():
    battery = psutil.sensors_battery()
    pr = str(battery.percent)
    if battery.power_plugged:
        return "Your system is currently charging and it's " + pr + "% done."
    return "Your system is currently on " + pr + "% battery life."

keyboard = Controller()
def mute():
	for i in range(50):
		keyboard.press(Key.media_volume_down)
		keyboard.release(Key.media_volume_down)

def full():
	for i in range(50):
		keyboard.press(Key.media_volume_up)
		keyboard.release(Key.media_volume_up)


def volumeControl(text):
	if 'full' in text or 'max' in text: full()
	elif 'mute' in text or 'min' in text: mute()
	elif 'incre' in text:
		for i in range(5):
			keyboard.press(Key.media_volume_up)
			keyboard.release(Key.media_volume_up)
	elif 'decre' in text:
		for i in range(5):
			keyboard.press(Key.media_volume_down)
			keyboard.release(Key.media_volume_down)

# Class to handle window operations
class WindowOpt:
    def __init__(self):
        self.keyboard = Controller()

    def openWindow(self):
        self.maximizeWindow()

    def closeWindow(self):
        self.keyboard.press(Key.alt_l)
        self.keyboard.press(Key.f4)
        self.keyboard.release(Key.f4)
        self.keyboard.release(Key.alt_l)

    def minimizeWindow(self):
        for _ in range(2):
            self.keyboard.press(Key.cmd)
            self.keyboard.press(Key.down)
            self.keyboard.release(Key.down)
            self.keyboard.release(Key.cmd)
            time.sleep(0.05)

    def maximizeWindow(self):
        self.keyboard.press(Key.cmd)
        self.keyboard.press(Key.up)
        self.keyboard.release(Key.up)
        self.keyboard.release(Key.cmd)

    def moveWindow(self, operation):
        self.keyboard.press(Key.cmd)

        if "left" in operation:
            self.keyboard.press(Key.left)
            self.keyboard.release(Key.left)
        elif "right" in operation:
            self.keyboard.press(Key.right)
            self.keyboard.release(Key.right)
        elif "down" in operation:
            self.keyboard.press(Key.down)
            self.keyboard.release(Key.down)
        elif "up" in operation:
            self.keyboard.press(Key.up)
            self.keyboard.release(Key.up)
        
        self.keyboard.release(Key.cmd)

    def switchWindow(self):
        self.keyboard.press(Key.alt_l)
        self.keyboard.press(Key.tab)
        self.keyboard.release(Key.tab)
        self.keyboard.release(Key.alt_l)


# Function to check if a text contains any of the words in the list
def isContain(text, lst):
    for word in lst:
        if word in text:
            return True
    return False

# Function to handle system tasks based on operation
def System_Opt(operation):
    s = SystemTasks()
    if isContain(operation, ['notepad', 'paint', 'calc', 'wordpad', 'word']):
        s.openApp(operation)

# Class to handle system tasks like opening applications
class SystemTasks:
    def openApp(self, appName):
        appName = appName.replace('paint', 'mspaint')
        appName = appName.replace('wordpad', 'write')
        appName = appName.replace('word', 'write')
        appName = appName.replace('calculator', 'calc')
        try:
            subprocess.Popen('C:\\Windows\\System32\\' + appName + '.exe')
        except Exception as e:
            print(f"Failed to open app: {e}")

# Function to handle window operations based on command
def Win_Opt(operation):
    w = WindowOpt()
    if isContain(operation, ['open']):
        w.openWindow()
    elif isContain(operation, ['close']):
        w.closeWindow()
    elif isContain(operation, ['mini']):
        w.minimizeWindow()
    elif isContain(operation, ['maxi']):
        w.maximizeWindow()
    elif isContain(operation, ['move', 'slide']):
        w.moveWindow(operation)
    elif isContain(operation, ['switch', 'which']):
        w.switchWindow()
        
		

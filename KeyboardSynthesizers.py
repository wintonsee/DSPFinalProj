from tkinter import *
import tkinter as Tk

import math
from math import *
import pyaudio
import numpy as np
from scipy import signal
import struct

BLOCKLEN   = 64        # Number of frames per block
WIDTH       = 2         # Bytes per sample
CHANNELS    = 1         # Mono
RATE        = 8000      # Frames per second

MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)

# Parameters
Ta = 2      # Decay time (seconds)
f1 = 250    # Frequency (Hz)
f0 = 440    # middle A

k = 0
fk = math.pow(2,k/12) * f0

r = 0.01**(1.0/(Ta*RATE))       # 0.01 for 1 percent amplitude
om1 = 2.0 * pi * float(fk)/RATE

# Filter coefficients (second-order IIR)
a1 = [1, -2*r*cos(om1), r**2]
b1 = [r*sin(om1)]

ORDER = 2   # filter order
states = np.zeros(ORDER)
x = np.zeros(BLOCKLEN)

# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = pyaudio.paInt16
stream = p.open(
        format      = PA_FORMAT,
        channels    = CHANNELS,
        rate        = RATE,
        input       = False,
        output      = True,
        frames_per_buffer = 128)

CONTINUE = True
KEYPRESS = False

################ GUI part ############
root = Tk.Tk()

def play(event):
    global CONTINUE
    global KEYPRESS
    global k,f0,fk, a1, b1
    print('You clicked at position (%d, %d)' % (event.x, event.y))
    #print('You pressed ' + event.char)
    if event.char == 'q':
      print('Good bye')
      CONTINUE = False
    KEYPRESS = True

    print(event.x)
    if (event.x<200):
        k = 1
        print("1")
    elif(event.x>=200 and event.x < 400):
        k = 2
        print("2")
    elif(event.x>=400 and event.x < 600):
        k = 3
        print("3")
    elif(event.x>=600 and event.x < 800):
        k = 4
        print("4")
    elif(event.x>=800 and event.x < 1000):
        k = 5       
        print("5")

    fk = math.pow(2,k/5) * f0

    om1 = 2.0 * pi * float(fk)/RATE
    a1 = [1, -2*r*cos(om1), r**2]
    b1 = [r*sin(om1)]


root.title('Keyboard Synthesizers')
root.configure(background= 'black')
root.geometry('1200x700')

topFrame = Frame(root, width = 200, height = 100)
topFrame.pack(side = TOP)
topFrame.configure(background='black')
bottomFrame = Canvas(root, width = 1000, height = 350)
bottomFrame.pack(side = BOTTOM, padx = 100)
bottomFrame.configure(background='white')


for i in range(5):
    xpos = 200 * i
    bottomFrame.create_line(xpos,0,xpos,350, width = 5)
    

topFrame.bind("<Button-1>",  play)
bottomFrame.bind("<Button-1>",  play)


while CONTINUE:
    root.update()

    if KEYPRESS:
        # Some key (not 'q') was pressed
        x[0] = 10000.0
    [y, states] = signal.lfilter(b1, a1, x, zi = states)
    x[0] = 0.0 

    KEYPRESS = False

    #y = y1
    y = np.clip(y.astype(int), -MAXVALUE, MAXVALUE)     # Clipping

    binary_data = struct.pack('h' * BLOCKLEN, *y)    # Convert to binary binary data
    stream.write(binary_data, BLOCKLEN)     



stream.stop_stream()
stream.close()
p.terminate()


#root.mainloop()
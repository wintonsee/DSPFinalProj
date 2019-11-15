from tkinter import *
import tkinter as Tk

import math
from math import *
import pyaudio
import numpy as np

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
    print('You clicked at position (%d, %d)' % (event.x, event.y))

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


root.mainloop()
# import the necessary library
from tkinter import *
import tkinter as Tk
from tkinter import messagebox

import math
from math import *
import pyaudio
import numpy as np
from scipy import signal
import struct

import time
import speech_recognition as sr


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

################ GUI part ##############
root = Tk.Tk()

# set a default value for piano-text

# need a string to store the input voice transfered string
text = "how are you"

# need a list to store the single character
textlist = ['h', 'o', 'w', 'a', 'r', 'e', 'y', 'o', 'u']

# a string to show what is playing currently
currenttext = ''

# a function use to play the voice when you press PLAY button
def play():
    global text, textlist

    # if the there are nothing inthe textlist, show messagebox.
    if not textlist:
        messagebox.showinfo("Warning", "We are run out of character! Please record more!")

    # after check the empty list, use the first character in the textlist to play the voice
    playchar(textlist[0])

    # show the current character poped out from textlist
    currentchar = textlist.pop(0)
    # change the currenttext
    currenttext.configure(text = str("Current Playing: " + currentchar))

    # change the textLabel and if it is space, skip the space
    if (text[0] == " "):
        text = text[2:]
    else:
        text = text[1:]
    textLebel.configure(text = text)

    # if text is empty, show warning message.
    if (text == ""): 
        textLebel.configure(text = "Press Record for more character!")
    print(text)

def playchar(ch):
    global KEYPRESS
    global k,f0,fk, a1, b1

    # in order to make voice, KEYPRESS must be True
    KEYPRESS = True

    # check if the current character is alpha or digit
    if(ch.isalpha()):
        # if it is digit, make it a number from 0-26
        outputch = ord(ch) - ord('a')
    elif(ch.isdigit()):
        # if it is alpha, make it a number from 27-36
        outputch = ord(ch) - ord('0') + 26
    else:
        # otherwise, make it 0
        outputch = 0
    
    print(outputch)

    # following code is us to change the voice 
    fk = math.pow(2,outputch/36) * f0

    om1 = 2.0 * pi * float(fk)/RATE
    a1 = [1, -2 * r * cos(om1), r ** 2]
    b1 = [r*sin(om1)]

    ### change the keyboard color to black, and back to white in 2 seconds.
    # check the position of current text number
    xpos = outputch *30+15
    # since the width of each key is 30, and width between is 2, 
    # so the width of changed color is 28
    bottomFrame.create_line(xpos,0,xpos,350, width = 28)
    # make the color disappear in 2 seconds with function colorchange, and position
    root.after(200, colorchange, xpos)

# function to change the color back to white
def colorchange(xpos):
    bottomFrame.create_line(xpos,0,xpos,350, width = 28, fill = 'white')

# function to record the user's voice and change to text
# when user press RECORD button
def record():
    global text, textlist

    # create a Recognizer Object
    r = sr.Recognizer()

    # make microphone as the voice source
    with sr.Microphone() as source:
        print('Speak something')
        # let Recognizer listen from microphone
        audio = r.listen(source, timeout = None)

        try: 
            # use Google Speech Recognition to transfer the voice to string message
            text = str(r.recognize_google(audio))
            textlist = []
            print("You said : {}".format(text))
        except:
            print("Sorry could not recognize your voice")

    # split the string to a list of word
    wordlist = text.split()

    # add characters to textlist by run word by word, and only add teh alpha or number character
    for word in wordlist:
        for char in word:
            if (char.isalnum()):
                textlist.append(char)

    # change the output textLabel to updated text
    textLebel.configure(text = text)
    print(textlist)

# function use to quit the game when user press QUIT button
def exitGame():
    global CONTINUE
    CONTINUE = False

### GUI's setting
root.title('Keyboard Synthesizers')
root.configure(background= 'black')
root.geometry('1200x700')

topFrame = Label(root, text = "Speech-Piano Music Creator\nECE 6183 DSP Lap\n Zikun Qian / Ziyi Xv", width = 80, font=("Times New Roman", 24, "bold"))
topFrame.pack(side = TOP)
topFrame.configure(background='white')

midFrame = Frame(root)
midFrame.pack(side = TOP, pady = 30)

textLebel = Label(midFrame, text = text)
textLebel.pack(side = TOP, pady = 10)

currenttext= Label(midFrame)
currenttext.pack(side = TOP, pady = 10)

midmidFrame = Frame(midFrame)
midmidFrame.pack(side = TOP, pady = 10)

recordButton = Button(midmidFrame, text = "Record", command = record, width = 20, height = 5)
recordButton.pack(side = LEFT, padx = 10)

playButton = Button(midmidFrame, text = "Play", command = play, width = 20, height = 5)
playButton.pack(side = RIGHT, padx = 10)

quitButton = Button(midFrame, text = "quit", command  = exitGame)
quitButton.pack(side = BOTTOM, padx = 10, pady = 10)

bottomFrame = Canvas(root, width = 1080, height = 350)
bottomFrame.pack(side = BOTTOM, padx = 60)
bottomFrame.configure(background='white')

# draw lines for different key on keyboard
for i in range(36):
    xpos = 30 * i
    bottomFrame.create_line(xpos,0,xpos,350, width = 2)
    

#topFrame.bind("<Button-1>",  play)
#bottomFrame.bind("<Button-1>",  play)


while CONTINUE:
    root.update()
    
    if KEYPRESS:
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
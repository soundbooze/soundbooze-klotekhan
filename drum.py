#
# blind drum reconstruction
#

import time

import os
import mido
import rtmidi
import random
import threading

drum = rtmidi.MidiOut()
drum.open_virtual_port("udukBot")

time.sleep(0.2)
os.system("aconnect 130:0 14:0")

'''

selling botDrummer [inmoov-like]

extreme booster: 

- servo linear-actuator
- proprietary midi-groove / vst / soundfonts

def NaiveBlindSourceSeparation():
    #print ('Todo')

def CurrentSegmentState():
    #segmentino(cyclicBuffer)

def BackgroundFeatureCompute():
    #print ('spectralFeatures ...')
    #PatternAlignment(recommendation)
    #Fill()

def GenrePrediction():
    via dynProg
'''

def Kick(s):
   velocity = random.randint(125, 127)
   note_on = [0x99, 36, velocity]
   note_off = [0x89, 36, 0]
   drum.send_message(note_on)
   drum.send_message(note_off)
   time.sleep(s)

def SnareStick(s):
   velocity = random.randint(126, 127)
   note_on = [0x99, 37, velocity]
   note_off = [0x89, 37, 0]
   drum.send_message(note_on)
   drum.send_message(note_off)
   time.sleep(s)

def Snare(s):
   velocity = random.randint(126, 127)
   note_on = [0x99, 38, velocity]
   note_off = [0x89, 38, 0]
   drum.send_message(note_on)
   drum.send_message(note_off)
   time.sleep(s)

def SnareEdge(s):
   velocity = random.randint(126, 127)
   note_on = [0x99, 40, velocity]
   note_off = [0x89, 40, 0]
   drum.send_message(note_on)
   drum.send_message(note_off)
   time.sleep(s)

def ClosedHiHat(s):
   velocity = random.randint(126, 127)
   note_on = [0x99, 42, velocity]
   note_off = [0x89, 42, 0]
   drum.send_message(note_on)
   drum.send_message(note_off)
   time.sleep(s)

def PedalHiHat(s):
   velocity = random.randint(126, 127)
   note_on = [0x99, 44, velocity]
   note_off = [0x89, 44, 0]
   drum.send_message(note_on)
   drum.send_message(note_off)
   time.sleep(s)

def SwishHiHat(s):
   velocity = random.randint(126, 127)
   note_on = [0x99, 48, velocity]
   note_off = [0x89, 48, 0]
   drum.send_message(note_on)
   drum.send_message(note_off)
   time.sleep(s)

def RideCymbalTip(s):
   velocity = random.randint(111, 114)
   note_on = [0x99, 51, velocity]
   note_off = [0x89, 51, 0]
   drum.send_message(note_on)
   drum.send_message(note_off)
   time.sleep(s)

def SplashCymbal(s):
   velocity = random.randint(103, 105)
   note_on = [0x99, 53, velocity]
   note_off = [0x89, 53, 0]
   drum.send_message(note_on)
   drum.send_message(note_off)
   time.sleep(s)

def CrashCymbal2(s):
   velocity = random.randint(110, 112)
   note_on = [0x99, 57, velocity]
   note_off = [0x89, 57, 0]
   drum.send_message(note_on)
   drum.send_message(note_off)
   time.sleep(s)

#
# 
# midi, rule-base, recommendation, static, evo, pre-generate ....
#
# bar predict , fill ... etc

def BeatVariation(b):

    print (b)

    if (b == 0):
        Kick(ts)
        Snare(ts)
        Kick(ts)
        Kick(ts)
        SnareStick(ts/2)
        Snare(ts/2)
        SnareEdge(ts)
        CrashCymbal2(ts)
    elif (b == 1):
        Kick(ts)
        Kick(ts)
        SplashCymbal(ts)
    elif (b == 2):
        PedalHiHat(ts)
        Kick(ts)
        SnareEdge(ts)
    elif (b == 3):
        PedalHiHat(ts)
        Kick(ts)
        SnareStick(ts)
    elif (b == 4):
        Kick(ts/2)
        Kick(ts/2)
        Snare(ts)
        SplashCymbal(ts)
        Snare(ts)
    elif (b == 5):
        Kick(ts)
        Snare(ts)
        Kick(ts)
        Kick(ts)
        Snare(ts)

BEATTXT = "/tmp/beat.txt"

while [ True ]:

    try:
        file = open(BEATTXT, "r") 
        ts = float(file.read())
        print (ts)
    except:
        pass

    # metal
    Kick(ts/4)
    Kick(ts/4)
    Kick(ts/4)
    Kick(ts/4)

    Snare(ts)
    BeatVariation(random.randint(0, 5))

del drum

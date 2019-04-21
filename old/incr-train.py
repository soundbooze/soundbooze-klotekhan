import time

import os
import mido
import rtmidi
import random

import sys
from mido import Message, MidiFile, MidiTrack

drum = rtmidi.MidiOut()
drum.open_virtual_port("udukBot")

time.sleep(0.2)
os.system("aconnect 130:0 14:0")

BEATTXT = "/tmp/beat.txt"

def ParseMIDI(filename):

    notes = []
    mid1 = MidiFile(filename)
    for i, track in enumerate(mid1.tracks):
            for msg in track:
                if not msg.is_meta:
                    s = str(msg).split(" ")
                    time = str(s[4]).split("=")
                    time = int(time[1])
                    try :
                        m = Message.from_bytes(msg.bytes())
                        #print(m.note, m.velocity, time)
                        notes.append(m.note);
                    except:
                        pass

    return notes

dataset = ['a.mid', 'b.mid', 'c.mid']

ts = 0.00090000000000000001

while [ True ]:

    try:
        file = open(BEATTXT, "r") 
        ts = float(file.read())
        print (ts)
    except:
        pass

    idd = random.randint(0, 2)
    notes = ParseMIDI(dataset[idd])
    velocity = random.randint(123, 127)

    for i, note in enumerate(notes):
        note_on = [0x99, note, velocity]
        note_off = [0x89, note, 0]
        drum.send_message(note_on)
        drum.send_message(note_off)

        ghost = random.randint(36, 48)
        note_on = [0x99, ghost, velocity]
        note_off = [0x89, ghost, 0]
        drum.send_message(note_on)
        drum.send_message(note_off)

        time.sleep(ts)

        ts = ts + 0.0001

del drum


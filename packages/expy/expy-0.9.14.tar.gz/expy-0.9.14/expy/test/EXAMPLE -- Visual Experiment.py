# coding:utf-8
##### package test #####
import sys
sys.path = ['../']+sys.path
################

from expy import *  # Import the needed functions
start()  # Initiate the experiment environment

def trial(word, pos):
    drawText(word, x=pos)  # Draw text on the canvas and display it

    key, rt = waitForResponse({key_.F: 'Left', key_.J: 'Right'}) # Waiting for pressing 'F' or 'J'
    if key == word:
        alertAndGo('Correct!', 1)  # Display something in 1s
    else:
        alertAndGo('Wrong!', 1)

    show(0.5)  # Pause (Keep displaying in 0.5s)


stimuli = [('Left', -0.5), ('Right', 0.5), ('Right', -0.5),
           ('Left', 0.5), ('Left', -0.5), ('Right', -0.5)]

instruction(shared.setting['instruction1'])
alertAndGo('The experiment will start after 3s.')  # Display something in 3s(default)

for word, pos in stimuli:
    trial(word, pos)  # Call the trial function with different parameters

alertAndQuit('Done!')  # Display something in 3s(default), and quit the program

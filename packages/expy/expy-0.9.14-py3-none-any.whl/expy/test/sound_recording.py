# coding:utf-8
##### package test #####
import sys
sys.path = ['../../']+sys.path
################

from expy import *  # Import the needed functions
start()  # Initiate the experiment environment

noise_level = environmentNoise(0.5)  # Detect the noise level of environment

'Without file'
textSlide('Recording: ')
sound, onset = recordSound(noise_level, rec_length_min=2, sound_length_max=6)
textSlide(f'Playing... (onset of last recording:{onset}) ')
playSound(sound)

'With file'
textSlide('Recording to file: ')
recordSound(noise_level, rec_length_min=2, sound_length_max=6, 
                                    path='data/record.WAV')
record = loadSound('data/record.WAV')
textSlide(f'Playing from file... (onset of last recording:{onset}) ')
playSound(record)

alertAndQuit('',0)
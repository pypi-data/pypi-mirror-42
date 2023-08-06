#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Filename : processAudio.py
# author by :tang
# python2.7
# platform:visual studio code, windows
# topic: 
# detial: process audio

import os
import subprocess
import numpy as np
import scipy.io.wavfile as wavfile
from audiolazy.lazy_lpc import lpc

#Extract audio from the video
def ffmpeg_extract_audio_from_video(out_path_audio ,input_path_video):
    cmd = 'ffmpeg -i %s -f wav -ar 16000 -ac 1 -y -vn %s' % (input_path_video ,out_path_audio)
    subprocess.call(cmd) #0
    ##Run the command described by args. Wait for command to complete, then return the returncode attribute.
    # subprocess.Popen(cmd) #<subprocess.Popen object at 0x0000000005861C88>

# 30fps 16kHz
def split_audio_chunks_of_520ms(input_path_wav , frames_per_second = 30):
    chunks_length = 260 #520ms
    rate,signal = wavfile.read(input_path_wav)
    if signal.dtype == 'int16':
        signal = signal / (2.**15)
    number_of_frames = frames_per_second * int(len(signal) / rate)
    frames_step = 1000.0 / frames_per_second
    rate_kHz = rate / 1000
    signal_insert = [0 for i in range(chunks_length*rate_kHz)] + signal + [0 for i in range(chunks_length*rate_kHz)]
    return [signal_insert[int((i*frames_step)*rate_kHz) : int((i*frames_step + 2*chunks_length)*rate_kHz)]
            for i in range(0,number_of_frames)],number_of_frames,rate

# The input audio window is divided into 64 audio frames with 2x overlap,
# so that each frame corresponds to 16ms (256 samples)
# and consecutive frames are located 8ms (128 samples) apart.
def divided_64_audio_frames_2x_overlap(signal,fs=16000,overlap_frames_apart = 0.008):
    overlap = int(fs*overlap_frames_apart) #128 samples
    frameSize = int(fs*overlap_frames_apart*2) #256 samples
    # numberOfframes = int(abs(len(signal) - frameSize) / overlap ) + 1
    numberOfframes = 64
    frames = np.ndarray((numberOfframes,frameSize))# initiate a 2D array with numberOfframes rows and frame size columns
    #assing samples into the frames (framing)
    for k in range(0,numberOfframes):
        for i in range(0,frameSize):
            if((k*overlap+i)<len(signal)):
                frames[k][i]=signal[k*overlap+i]
            else:
                frames[k][i]=0
    # remove the DC component
    # frames = [(frames[k] - np.mean(frames[k])) for k in range(0,numberOfframes)]
    
    # apply the standard Hann window to reduce temporal aliasing effects
    frames*=np.hanning(frameSize)
    # calculate K = 32 autocorrelation coefficients to yield a total of 64×32 scalars for the input audio window.
    # if list is [0,0,0,...,0,0] or [0,0,0,...,0,1] ,lpc will return:[]
    return frames,[lpc(frames[i],order=32).numerator[1:] for i in range(0,numberOfframes)]
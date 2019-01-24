#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DTW based TextGrid adaptation.

Based on DTW and librosa modules and using the TextGrid tools (tgt). The code was written following the example code on Using DTW to compare sounds
https://github.com/pierre-rouanet/dtw/blob/master/examples/MFCC%20%2B%20DTW.ipynb

Created on Thu Nov 2 10:43:55 2017

@author: gerazov

Copyright 2017 by GIPSA-lab, Grenoble INP, Grenoble, France.

See the file LICENSE for the licence associated with this software.
"""

import numpy as np
from matplotlib import pyplot as plt
import librosa
from dtw import dtw
from numpy.linalg import norm
import tgt  # textgrid tools
from scipy.interpolate import interp1d
from datetime import datetime
import sys

start_time = datetime.now()

#%% define the source and target files
data_folder = '../data/modalities/'
textgrid_folder = data_folder
# source
barename_src = 'declaration'
wav_src = barename_src+ '.wav'
textgrid_src =  barename_src+'.TextGrid'
# targets - list of target files
targets = [
           # 'question',
           'incredulous',
           # 'fascinated',
           # 'irony',
           # 'scandalised',
           ]

#%% define parameters
# default hop = 512,
hop = 32
plot = False

#%% loop through target files
for barename_dest in targets:
    wav_dest = barename_dest+'.wav'
    print('\nProcessing file {}'.format(wav_dest))
    textgrid_dest =  barename_dest+'.TextGrid'

    #%%% read audio and find mfccs
    filename_src = data_folder + wav_src
    filename_dest = data_folder + wav_dest
    #% load waves (librosa automatically resamples to 22k)
    y1, sr1 = librosa.load(filename_src)
    t1 = np.arange(0, y1.size)/sr1
    y2, sr2 = librosa.load(filename_dest)
    t2 = np.arange(0, y2.size)/sr2
    t_max = np.max((t1[-1], t2[-1])) # add extra margin
    print('Calculating mfccs ...')
    mfcc1 = librosa.feature.mfcc(y1, sr1, hop_length=hop)
    mfcc2 = librosa.feature.mfcc(y2, sr2, hop_length=hop)
    hop_t = hop/sr1
    t_frames1 = np.arange(0,mfcc1.shape[1]*hop_t, hop_t)
    hop_t = hop/sr2
    t_frames2 = np.arange(0,mfcc2.shape[1]*hop_t, hop_t)

    #%%% do the DTW
    print('Calculating dtw path ...')
    dist, cost, cost_acc, path = dtw(mfcc1.T,
                                     mfcc2.T,
                                     dist=lambda x, y: norm(x - y, ord=1))
    t_frame_src = t_frames1[path[0]]
    t_frame_dest = t_frames2[path[1]]

    #% plot DTW
    if plot:
        plt.figure()
        plt.imshow(cost.T, extent=[0, t_frames1[-1], 0, t_frames2[-1]],
                   origin='lower', cmap='gray', interpolation='bilinear')
        plt.plot(t_frame_src, t_frame_dest, 'w')
        plt.title('DTW map between {} and {}.'.format(barename_src,
                                                      barename_dest))
    # now t for interpolation
    t_in = np.arange(0,t_max + .02,.001)  # as ms, add extra margin
    interfunc = interp1d(t_frame_src, t_frame_dest, kind='nearest',
                         bounds_error=False, fill_value='extrapolate')
    t_out = interfunc(t_in)

    #%%% do the text grids
    print('\nProcessing text grids ...')
    try:
        textgrid = tgt.read_textgrid(data_folder + textgrid_src,
                                     encoding='utf-16')
    except:
        print(sys.exc_info()[0])
        raise

    for tier in textgrid.tiers:
        if tier.tier_type() == 'IntervalTier':
            for i, interval in enumerate(tier.intervals):
                try:
                    interval.end_time = t_out[int(interval.end_time * 1000)]
                except:
                    print('Setting interval.end_time to t_out')
                    interval.end_time = t2[-1]
                interval.start_time = t_out[int(interval.start_time * 1000)]
        else:
            for point in tier.points:
                point.time = t_out[int(point.time * 1000)]
        try:
            tier.end_time = t_out[int(tier.end_time * 1000)]
        except:
            print('Setting tier.end_time to t_out')
            tier.end_time = t2[-1]

    tgt.write_to_file(textgrid, data_folder + textgrid_dest, format='long',
                      encoding='utf-16')

#%% wrap up
end_time = datetime.now()
dif_time = end_time - start_time
print('Finished all in {}'.format(dif_time))

# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 21:25:24 2014

@author: Polina
"""

import numpy as np
import matplotlib.pylab as plt


def load(filename):
    """
    load a file in memory (leaving DATA aside for now)
    """
    data = np.load(filename)    
    nb_samples = data['DATA']

    return len(nb_samples[0]), int(data['srate']), data['stages']

def load_all():
    """
    load all the subject files and produce two subject dicts for each state (baseline & sleep depravation)
    a subject item is a list of following attributes:
        - samples = number of samples (number of columns inside DATA array)
        - srate = sampling rate
        - stages = array of stages
    """
    subjects_BSL = {}
    subjects_REC = {}
 
    for i in range(1,5):
        key = 'S' + str(i)
        filename = key + '_BSL.npz'
        samples, srate, stages = load(filename)        
        subjects_BSL[key] = [samples, srate, stages]
        filename = key + '_REC.npz'
        samples, srate, stages = load(filename)        
        subjects_REC[key] = [samples, srate, stages]
        
    return subjects_BSL, subjects_REC

    
def plot_stages(srate, stages_bsl, stages_rec, subjectNum):
    #time = np.arange(30,int(len(eeg)/srate + 30),30)
    #time = np.arange(30,int(samplesLen/srate + 30),30)
    
    filteredStages_bsl = stages_bsl[stages_bsl < 6]
    filteredStages_rec = stages_rec[stages_rec < 6] 

    nightTime_bsl = np.arange(30,(len(filteredStages_bsl)+1)*30,30)
    nightTime_rec = np.arange(30,(len(filteredStages_rec)+1)*30,30)
    xticks = np.arange(1800, (len(filteredStages_bsl)+1)*30, 1800)
   
    plt.plot(nightTime_bsl, filteredStages_bsl, drawstyle='steps', hold='true',c="g")
    plt.plot(nightTime_bsl, filteredStages_rec[0:len(filteredStages_bsl)], drawstyle='steps',c="r")
    plt.ylim(0,5.5)
    
    plt.xticks(xticks)
    plt.xlabel('Time (sec)')
    plt.ylabel('Stages (0 - 5)')
    plt.legend(['BSL','REC'],loc='top right')
    plt.title('Subject '+ str(subjectNum))
    

    ##########################
#You can put the code that calls the above functions down here    
if __name__ == "__main__":
    s_bsl1, srate1, stages_bsl1 = load('S1_BSL.npz')
    s_rec1, srate1, stages_rec1 = load('S1_REC.npz')    

    """
    s_bsl2, srate2, stages_bsl2 = load('S2_BSL.npz')
    s_rec2, srate2, stages_rec2 = load('S2_REC.npz')    
    
    s_bsl3, srate3, stages_bsl3 = load('S3_BSL.npz')
    s_rec3, srate3, stages_rec3 = load('S3_REC.npz')    
    
    s_bsl4, srate4, stages_bsl4 = load('S4_BSL.npz')
    s_rec4, srate4, stages_rec4 = load('S4_REC.npz')
  
    """
    plot_stages(srate1, stages_bsl1, stages_rec1,1)
    
    """
    plot_stages(srate2, stages_bsl2, stages_rec2,2)
    plot_stages(srate3, stages_bsl3, stages_rec3,3)
    plot_stages(srate4, stages_bsl4, stages_rec4,4)
    """
    #load_all()

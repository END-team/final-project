#
#  NAME
#    problem_set4.py
#
#  DESCRIPTION
#    In Problem Set 4, you will classify EEG data into NREM sleep stages and
#    create spectrograms and hypnograms.
#
from __future__ import division
import gc
import numpy as np
import matplotlib.pylab as plt
import matplotlib.mlab as m
from matplotlib.colors import ListedColormap
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.lda import LDA
from sklearn.qda import QDA
from copy import deepcopy

def load_REM_from_file(filename):
    """
    load_file takes the file name and reads in the data.  It returns an
    array containing sleep stages in minutes NREM S1, S2, S3, S4, REM
    """
    gc.collect()    
    data = np.load(filename)
    a = data['stages']
    d = data['DATA']
    srate = data['srate']
    j=0
    it = np.nditer(a, flags=['f_index'])
    while not it.finished:
        if( it[0]==5 ):
            eeg = pull_epoch(d, srate, it.index)
            if(j==0):
                samples = eeg
            else:
                samples = np.hstack((samples,eeg))
            j=j+1
        it.iternext()
    return samples, srate
    
def pull_epoch(data, srate, epoch_number):
    elength = srate * 30.0
    startpos = epoch_number * elength
    endpos = startpos + elength
    eegdata = data[0:,int(startpos):int(endpos)]
    return eegdata

def plot_spectrograms(bsl,rec,rate,title):
    plt.close()
    fig, ax = plt.subplots(nrows=9, ncols=2, sharex=True, sharey=True)
    ny_nfft=1024
    i=0
    while i<9:
        Pxx, freq, bins, im = ax[i,0].specgram(bsl[i],NFFT=ny_nfft,Fs=rate)
        #ax[i,0].ylim(0,40)
        ax[i,0].set_xlim([0, 40])
        ax[i,0].set_xlabel("Time, seconds")
        ax[i,0].set_ylabel("Freq, Hz")
        ax[i,0].set_title(title+'baseline sleep, REM stage, Channel:'+str(i+1))
        i=i+1
    i=0
    while i<9:
        Pxx, freq, bins, im = ax[i,1].specgram(rec[i],NFFT=ny_nfft,Fs=rate)
        #ax[i,1].ylim(0,40)
        ax[i,0].set_xlim([0, 40])
        ax[i,1].set_xlabel("Time, seconds")
        ax[i,1].set_ylabel("Freq, Hz")
        ax[i,1].set_title(title+'recovery sleep, REM stage, Channel:'+str(i+1))
        i=i+1
    plt.show()
    return

##########################
#You can put the code that calls the above functions down here    
if __name__ == "__main__":
    j = 1    
    while j<5:
        BSL_REM, srate = load_REM_from_file('S'+str(j)+'_BSL.npz')
        REC_REM, srate = load_REM_from_file('S'+str(j)+'_REC.npz')
        plot_spectrograms(BSL_REM,REC_REM,srate,'Subject '+str(j))
        j=j+1
    plt.close('all') #Closes old plots.

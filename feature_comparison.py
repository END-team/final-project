#
#  NAME
#    feature_selection.py
#
#  DESCRIPTION
#    see https://github.com/END-team/final-project/wiki
#    datasets should be located in the same folder
#
from __future__ import division
import gc
import numpy as np
import matplotlib.pylab as plt


def load_REM_from_file(filename):
    """
    load_file takes the file name and reads in the data.  It returns an
    array containing only REM sleep stage
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

def plot_spectrograms(bsl,rec,rate,y,ax):
    ny_nfft=1024
    i=7
    plt.tick_params(axis='both', labelsize=8)

    Pxx, freq, bins, im = ax[y,0].specgram(bsl[i],NFFT=ny_nfft,Fs=rate)
    ax[y,0].set_yticks(np.arange(0, 50, 10))
    ax[y,0].set_ylim([0, 40])
    if(y==3):
        ax[y,0].set_xlabel("Time, seconds", fontsize=10)
    ax[y,0].set_ylabel("Freq, Hz", fontsize=8)
    ax[y,0].set_title('Subject '+str(y+1)+' Baseline', fontsize=10)
    for label in (ax[y,0].get_xticklabels() + ax[y,0].get_yticklabels()):
        label.set_fontname('Arial')
        label.set_fontsize(8)

    Pxx, freq, bins, im = ax[y,1].specgram(rec[i],NFFT=ny_nfft,Fs=rate)
    ax[y,0].set_yticks(np.arange(0, 50, 10))
    ax[y,1].set_ylim([0, 40])
    #ax[i,1].set_xlim([0, 10000]) #13000])
    if(y==3):
        ax[y,1].set_xlabel("Time, seconds", fontsize=10)
    #ax[i,1].set_ylabel("Freq, Hz")
    ax[y,1].set_title('Subject '+str(y+1)+' Recovery', fontsize=10)
    for label in (ax[y,0].get_xticklabels() + ax[y,0].get_yticklabels()):
        label.set_fontname('Arial')
        label.set_fontsize(8)

    
    return

##########################
#You can put the code that calls the above functions down here    
if __name__ == "__main__":
    plt.close('all') #Closes old plots.

    plt.rc('font', family='Arial')
    fig, ax = plt.subplots(nrows=4, ncols=2, sharex='col', sharey='row')
    fig.suptitle("Comparison of REM stages - Baseline vs. Recovery Sleep for channel 8 (C4/A1)", fontsize=20)
    plt.subplots_adjust(wspace = .05,hspace = 0.4 )

    j = 1    
    while j<5:
        BSL_REM, srate = load_REM_from_file('S'+str(j)+'_BSL.npz')
        REC_REM, srate = load_REM_from_file('S'+str(j)+'_REC.npz')
        plot_spectrograms(BSL_REM,REC_REM,srate,j-1,ax)
        j=j+1

    plt.show()
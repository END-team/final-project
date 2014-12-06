#
#  NAME
#    final_problem_summary.py
#
#  DESCRIPTION
#    see https://github.com/END-team/final-project/wiki
#    datasets should be located in the same folder
#
from __future__ import division
import numpy as np
import matplotlib.pylab as plt
import pandas as pd


def load_file(filename):
    """
    load_file takes the file name and reads in the data.  It returns an
    array containing sleep stages in minutes NREM S1, S2, S3, S4, REM
    """
    data = np.load(filename)
    a = data['stages']
    return np.array( [a[a==1].size, a[a==2].size, a[a==3].size, a[a==4].size, a[a==5].size] )/2


##########################
if __name__ == "__main__":

    plt.close('all')

    bsl = np.hstack((load_file('S1_BSL.npz'), load_file('S2_BSL.npz'), load_file('S3_BSL.npz'), load_file('S4_BSL.npz')))
    rec = np.hstack((load_file('S1_REC.npz'), load_file('S2_REC.npz'), load_file('S3_REC.npz'), load_file('S4_REC.npz')))
    
    stage = ['NREM S1','NREM S2','NREM S3','NREM S4','REM']*4
    subject = np.repeat(['Subj 1', 'Subj 2', 'Subj 3', 'Subj 4'], [5, 5, 5, 5], axis=0)
    ix3 = pd.MultiIndex.from_arrays([stage, subject], names=['stage', 'subject'])

    df3 = pd.DataFrame({'BSL': bsl, 'REC': rec}, index=ix3)   
    gp3 = df3.groupby(level=('stage', 'subject'))
    df3.plot( kind='barh')
    plt.title('Baseline vs. Recovery sleep By Sleep Stage and Subject')
    plt.ylabel('Sleep Stage/Subject')
    plt.xlabel('Time, minutes')
    plt.legend(loc='upper right')
    
    gp4 = df3.groupby(level=('stage'))
    means = gp4.mean()
    errors = gp4.std()
    fig, ax = plt.subplots()
    means.plot(yerr=errors, ax=ax, kind='bar')
    plt.title('Baseline vs. Recovery Sleep Stage Means with Errors')
    plt.ylabel('Sleep Stage')
    plt.xlabel('Time, minutes')
    plt.legend(loc='upper right')
    
    plt.show()
    
    df3['bsl_sum'] = df3.BSL.cumsum()
    df3['rec_sum'] = df3.REC.cumsum()
    df3['bsl_perc'] = 100*df3.bsl_sum/df3.BSL.sum()


    

    



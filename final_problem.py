#
#  NAME
#    final_problem.py
#
#  DESCRIPTION
#    see https://github.com/END-team/final-project/wiki
#    datasets should be located in the same folder
#
from __future__ import division
import numpy as np
import matplotlib.pylab as plt
import pandas as pd


def load_eeg(filename):
    """
    load_eeg takes the file name and reads in the data.  It returns an
    array containing EEG data and the sampling rate for
    the data in Hz (samples per second).
    """
    data = np.load(filename)
    #return data['DATA'], int(data['srate']), data['stages']
    return data['stages']

def load_df(a, subject_id, sample_type):
    # Create a DataFrame to organize our data
    df = pd.DataFrame()

    #all data
    #df['stage'] = np.arange(0,8)
    #df['count'] = np.array( [a[a==0].size, a[a==1].size, a[a==2].size, a[a==3].size, a[a==4].size, a[a==5].size, a[a==6].size, a[a==7].size] )
    #df['subject'] = [subject_id for x in range(8)]
    #df['test'] = [sample_type for x in range(8)]

    df['stage'] = ['NREM S1','NREM S2','NREM S3','NREM S4','REM']
    df['count'] = np.array( [a[a==1].size, a[a==2].size, a[a==3].size, a[a==4].size, a[a==5].size] )/2
    df['subject'] = [subject_id for x in range(5)]
    df['test'] = [sample_type for x in range(5)]
    
    return df

def plot_stages(df):
    #results = df.pivot_table(values='count', index=['test'], columns='subject')

    #results = df.pivot_table(index=['test'], columns='subject')
    results = df.pivot_table(values='count',index=['stage','subject'], columns='test')
    results.plot(kind='barh')

    #by_keys = df.groupby(['stage','test','subject'])
    #by_keys.mean().plot(kind='bar', stacked=True)

    # And add plot details (title, legend, xlabel, and ylabel)
    plt.title('Baseline sleep vs. Recovery sleep')
    plt.ylabel('Sleep stage/Subject')
    plt.xlabel('Time, minutes')
    plt.legend(loc='upper right')
    
    plt.show()
    return
    

##########################
if __name__ == "__main__":
    #YOUR CODE HERE
    s1_bsl_stages = load_eeg('S1_BSL.npz')
    s1_rec_stages = load_eeg('S1_REC.npz')
    s2_bsl_stages = load_eeg('S2_BSL.npz')
    s2_rec_stages = load_eeg('S2_REC.npz')
    s3_bsl_stages = load_eeg('S3_BSL.npz')
    s3_rec_stages = load_eeg('S3_REC.npz')
    s4_bsl_stages = load_eeg('S4_BSL.npz')
    s4_rec_stages = load_eeg('S4_REC.npz')
    
    df_s1_bsl = load_df(s1_bsl_stages, 'Subj 1', 'BSL')
    df_s1_rec = load_df(s1_rec_stages, 'Subj 1', 'REC')
    df_s2_bsl = load_df(s2_bsl_stages, 'Subj 2', 'BSL')
    df_s2_rec = load_df(s2_rec_stages, 'Subj 2', 'REC')
    df_s3_bsl = load_df(s3_bsl_stages, 'Subj 3', 'BSL')
    df_s3_rec = load_df(s3_rec_stages, 'Subj 3', 'REC')
    df_s4_bsl = load_df(s4_bsl_stages, 'Subj 4', 'BSL')
    df_s4_rec = load_df(s4_rec_stages, 'Subj 4', 'REC')
    
    df = pd.concat([df_s1_bsl, df_s1_rec, df_s2_bsl, df_s2_rec, df_s3_bsl, df_s3_rec, df_s4_bsl, df_s4_rec])

    plt.close('all')
    plot_stages(df)


    

    



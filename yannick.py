# -*- coding: utf-8 -*-
"""
Created on Sat Nov 29 08:12:48 2014

@author: yannick
"""


import numpy as np
import pandas as pd
import matplotlib.pylab as plt


def load(filename):
    """
    load a file in memory (leaving DATA aside for now)
    """
    data = np.load(filename)    
    nb_samples = data['DATA']
#    return data['DATA'], int(data['srate']), data['stages']
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

def first_analyse(base, depr):
    """
    Code used for initial exploration - no more relevant    
    """
    df = pd.DataFrame()
    samplesN = np.zeros(4)
    samplesD = np.zeros(4)    
    stagesN = np.zeros(4)
    stagesD = np.zeros(4)
    
    for i in range(1,5):
        samplesN[i-1] = base['S' + str(i)][0]        
        samplesD[i-1] = depr['S' + str(i)][0]
        stagesN[i-1] = len(base['S' + str(i)][2])
        stagesD[i-1] = len(depr['S' + str(i)][2])
  
    df['samples normal'] = samplesN
    df['stages normal'] = stagesN
    df['samples depravation'] = samplesD
    df['stages depravation'] = stagesD
    df['epoch normal'] = df['samples normal'] / df['stages normal']
    df['epoch depravation'] = df['samples depravation'] / df['stages depravation']
    
    freq = np.zeros((4,9)) # stage frequency (ie # of occurence of stage 0, stage 1 etc...)
    for i in range(1,5):
        for j in range(0,8):
            freq[i-1, j] = list(base['S' + str(i)][2]).count(j)
#            test[i-1] = len(np.where(base['S' + str(i)][2]) == j)[0]
        print freq[i-1]
    print freq    
#    df['stage frequency (Normal)'] = freq[:,]
    
    return df


def analyse(subjects):
    """
    Adding basic computation to help interpreting the information
    """
    df = pd.DataFrame()
    samples = np.zeros(4)
    stages = np.zeros(4)
    duration = np.zeros(4)
    
    for i in range(1,5):
        samples[i-1] = subjects['S' + str(i)][0]        
        stages[i-1] = len(subjects['S' + str(i)][2])
        duration[i-1] = len(subjects['S' + str(i)][2]) * 30.0 / 3600
  
    df['samples'] = samples
    df['stages'] = stages
    df['epoch'] = df['samples'] / subjects['S' + str(i)][1]  / df['stages']
#    df['sleep duration'] = samples / subjects['S' + str(i)][1] / 3600
    df['sleep duration'] = duration

    
    freq = np.zeros(4) # stage frequency (ie # of occurence of stage 0, stage 1 etc...)

    for i in range(0,8):
        for j in range(1,5):
            freq[j-1] = list(subjects['S' + str(j)][2]).count(i)
        df['s' + str(i)] = freq
        df['%' + str(i)] = freq / df['stages'] * 100
         
    total_transitions = 0
    ttab = np.zeros((4,64))
    for k in range(0,4):
        l = list(subjects['S' + str(k+1)][2])
        tmp = np.zeros((8,8))    
        current = l[0]
        for i in range(0, len(l)):
            stg = l[i]
            if (stg < 6) & (stg <> current):
                tmp[current, stg] = tmp[current, stg] + 1  
                current = stg
                total_transitions = total_transitions + 1
        t = np.reshape(tmp, 64)
        ttab[k] = t
    
    for i in range(0,6): # do not care about stage transitions > 5
        for j in range(0,6):
            col = ttab[:,(i*8)+j]
            df['t' + str(i) + '-' + str(j)] = col
            df['%t' + str(i) + '-' + str(j)] = col / total_transitions * 100   
    return df

def plot_histogram(df1, df2):
    """
    plot histo for question 1 (Difference in REM sleep?)
        result => not concluant
    df1: normal sleep (df1 = analyse(base))
    df2: sleep depravation (df2 = analyse(depr))
    """    
    plt.rc('font', family='Arial')
    N = 5
    normal = df1['%5'].tolist()
    mean = sum(normal) / len(normal)
    normal.extend([mean])

    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, normal, width, color='b')

    depravation = df2['%5'].tolist()
    mean = sum(depravation) / len(depravation)
    depravation.extend([mean])


    rects2 = ax.bar(ind+width, depravation, width, color='r')

    ax.set_ylabel('Sleep in REM stage (%)')
    ax.set_xlabel('Subjects')
    
    ax.set_title('REM sleep comparison', fontsize=20)
    ax.set_xticks(ind+width)
    ax.set_xticklabels( ('1', '2', '3', '4', 'Mean') )
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
           label.set_fontname('Arial')
           label.set_fontsize(8)            

    ax.legend( (rects1[0], rects2[0]), ('Baseline', 'After sleep depravation') ,  loc = 'lower right', fontsize=10 )
    
def plot_sleepTime(df1, df2):
    """
    First conclusion - obvious from experience -> sleep time longer after sleep depravation
    df1: normal sleep (df1 = analyse(base))
    df2: sleep depravation (df2 = analyse(depr))
    """    

    plt.rc('font', family='Arial')
    N = 5
    normal = df1['sleep duration'].tolist()
    mean = sum(normal) / len(normal)
    normal.extend([mean])

    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, normal, width, color='b')

    depravation = df2['sleep duration'].tolist()
    mean = sum(depravation) / len(depravation)
    depravation.extend([mean])


    rects2 = ax.bar(ind+width, depravation, width, color='r')

    ax.set_ylabel('Sleep time (hours)')
    ax.set_xlabel('Subjects')
    
    ax.set_title('Overall sleep duration comparison', fontsize=20)
    ax.set_xticks(ind+width)
    ax.set_xticklabels( ('1', '2', '3', '4', 'Mean') )
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
           label.set_fontname('Arial')
           label.set_fontsize(8)            

    ax.legend( (rects1[0], rects2[0]), ('Baseline', 'Recovery'), loc = 'lower right', fontsize=10 )    

def plot_transition(df1, df2):
    """
    plot stage transitions
    df1: normal sleep (df1 = analyse(base))
    df2: sleep depravation (df2 = analyse(depr))
    """    
    N = 5
    ind = np.arange(N)  # the x locations for the groups
    width = 0.2       # the width of the bars
    plt.close()
    plt.rc('font', family='Arial')

    fig, ax = plt.subplots(nrows=6, ncols=6, sharex='col', sharey='row')
    fig.suptitle("Comparison of the number of stage transitions, (origin stage " + u'\u2192' + " dest. stage)", fontsize=20)        
    plt.subplots_adjust(wspace = 0.2,hspace = 0.4 )
    for i in range(0,6): # do not care about stage transitions > 5
        for j in range(0,6):     
            clef = 't' + str(i) + '-' + str(j)
            normal = df1[clef].tolist()
            mean = sum(normal) / len(normal)
            normal.extend([mean])
            rects1 = ax[i,j].bar(ind, normal, width, color='b')
            depravation = df2[clef].tolist()
            mean = sum(depravation) / len(depravation)
            depravation.extend([mean])
            rects2 = ax[i,j].bar(ind+width, depravation, width, color='r')
            for label in (ax[i,j].get_xticklabels() + ax[i,j].get_yticklabels()):
                label.set_fontname('Arial')
                label.set_fontsize(8)            
            ax[i,j].set_title(str(i) + ' ' + u'\u2192' + ' ' + str(j))
            ax[i,j].set_xticks(ind+width)
            ax[i,j].set_xticklabels( ('1', '2', '3', '4', 'Avg') )
            ax[i,j].set_yticks(np.arange(0, 50, 10))
            ax[i,j].set_ylim([0,45])
    fig.legend( (rects1[0], rects2[0]), ('Baseline', 'Recovery'), loc = 'lower right', fontsize=10)

def plot_transition_ratio(df1, df2):
    """
    plot stage transitions
    df1: normal sleep (df1 = analyse(base))
    df2: sleep depravation (df2 = analyse(depr))
    """    
    N = 5
    ind = np.arange(N)  # the x locations for the groups
    width = 0.2       # he width of the bars
    plt.close()
    plt.rc('font', family='Arial')

    fig, ax = plt.subplots(nrows=6, ncols=6, sharex='col', sharey='row')
    fig.suptitle("Comparison of the number of stage transitions (% of total transitions) (origin stage " + u'\u2192' + " dest. stage)", fontsize=20)        
    plt.subplots_adjust(wspace = 0.2,hspace = 0.4 )
    for i in range(0,6): # do not care about stage transitions > 5
        for j in range(0,6):     
            clef = '%t' + str(i) + '-' + str(j)
            normal = df1[clef].tolist()
            mean = sum(normal) / len(normal)
            normal.extend([mean])
            rects1 = ax[i,j].bar(ind, normal, width, color='b')
            depravation = df2[clef].tolist()
            mean = sum(depravation) / len(depravation)
            depravation.extend([mean])
            rects2 = ax[i,j].bar(ind+width, depravation, width, color='r')
            for label in (ax[i,j].get_xticklabels() + ax[i,j].get_yticklabels()):
                label.set_fontname('Arial')
                label.set_fontsize(8)            
            ax[i,j].set_title(str(i) + ' ' + u'\u2192' + ' ' + str(j))
            ax[i,j].set_xticks(ind+width)
            ax[i,j].set_xticklabels( ('1', '2', '3', '4', 'Avg') )
            ax[i,j].set_yticks(np.arange(0, 6, 2))
            ax[i,j].set_ylim([0,6])
    fig.legend( (rects1[0], rects2[0]), ('Baseline', 'Recovery'), loc = 'lower right', fontsize=10)


if __name__ == "__main__":
# Uncomment next to reload the files (needed to run once)
#    base, depr = load_all()
    df1 = analyse(base)
    df2 = analyse(depr)
#    plot_histogram(df1, df2)
#    plot_sleepTime(df1, df2)
#    plot_transition(df1, df2)
    plot_transition_ratio(df1, df2)
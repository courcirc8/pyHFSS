# -*- coding: utf-8 -*-
"""
Created on Sat Feb 04 09:32:46 2017

@author: Minev
"""
from __future__ import print_function    # Python 2.7 and 3 compatibility
import warnings
import numpy as np
import pandas as pd

from scipy.constants import *
from scipy.constants import hbar, e as e_el, epsilon_0, pi

### Constants
fluxQ = hbar / (2*e_el)
warnings.filterwarnings('ignore', category=pd.io.pytables.PerformanceWarning)

#==============================================================================
# Utility functions
#==============================================================================

def fact(n):
    if n <= 1:
        return 1
    return n * fact(n-1)

def nck(n, k):
    return fact(n)/(fact(k)*fact(n-k))

def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used."""
    def newFunc(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning) #turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__), category=DeprecationWarning, stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning) #reset filter
        return func(*args, **kwargs)
    newFunc.__name__ = func.__name__
    newFunc.__doc__ = func.__doc__
    newFunc.__dict__.update(func.__dict__)
    return newFunc


def print_matrix(M, frmt = "{:7.2f}", append_row = ""):
    M = np.mat(M)
    for row in np.array(M.tolist()):
        print(' ', end='')
        for chi in row:
            print( frmt.format(chi), end='')
        print( append_row+"\n", end='')

def divide_diagonal_by_2(CHI0):
    CHI = CHI0.copy();
    CHI[np.diag_indices_from(CHI)] /= 2
    return CHI;

def print_NoNewLine(text):
    print((text), end='')

def print_color(text, style = 0, fg=24, bg = 43, newline = True):
    '''style 0..8;   fg  30..38;  bg  40..48'''
    format = ';'.join([str(style), str(fg), str(bg)])
    s = '\x1b[%sm %s \x1b[0m' % (format, text)
    if newline:
        print(s)
    else:
        print(s, end='')


#==============================================================================
#%%         Dataframe
#==============================================================================

def DataFrame_col_diff(PS, indx=0):
    ''' check weather the columns of a dataframe are equal,
        returns a T/F series of the row index that specifies which rows are differnt
        USE:
            PS[DataFrame_col_diff(PS)]
    '''
    R = []
    for i in range(PS.shape[1]-1):
        R += [ PS.iloc[:,i] == PS.iloc[:,i+1] ]
    if len(R) == 1:
        return np.logical_not(R[0])
    else:
        return np.logical_not(np.logical_and.reduce(R))



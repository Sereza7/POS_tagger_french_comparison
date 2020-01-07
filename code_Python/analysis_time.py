# -*- coding: utf-8 -*-
import sys
sys.path.append('/Users/lucas/Desktop/CodeV/code_Python')

import os
import spacy
import treetaggerwrapper
import analysis_parsers as analysis
import analyse_FTB as callall
spacy_nlp = spacy.load("fr_core_news_sm")
from subprocess import (PIPE, Popen)
import cProfile



def invoke(command):
    '''
    Invoke command as a new system process and return its output.
    '''
    pr = cProfile.Profile()
    pr.enable
    result= Popen(command, stdout=PIPE, shell=True).stdout.readlines()
    pr.disable()
    ps = pstats.Stats(pr, stream=StringIO.StringIO()).sort_stats('cumulative')
    return result

def print_times(file_dir,out_dir):
    callall.saveanalysis(file_dir,out_dir)

    


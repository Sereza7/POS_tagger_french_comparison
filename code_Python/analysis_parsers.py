# -*- coding: utf-8 -*-
import sys
import os
import spacy
import treetaggerwrapper
spacy_nlp = spacy.load("fr_core_news_sm")
from subprocess import (PIPE, Popen)
import cProfile,pstats
from memory_profiler import memory_usage,profile   #profiler for the memory, https://pypi.org/project/memory-profiler/ ;not used in the study

timeanalysis=False

def invoke(command):
    '''
    Invoke command as a new system process and return its output.
    If timeanalysis == true, also print the time spent on the command
    '''
    pr = cProfile.Profile()
    pr.enable()
    result= Popen(command, stdout=PIPE, shell=True).stdout.readlines()
    pr.disable()
    if timeanalysis==True:
        print(command[:30])
        ps = pstats.Stats(pr).sort_stats("cumulative").print_stats()
    return result
    


@profile
def POS_5_print(sample):
    '''
    Print the results of the 5 taggers to the text sample
    '''
    #first, get the result from the algorithms
    r=[]
    pr = cProfile.Profile()
    pr.enable()
    r.append(spacy_POS(sample))
    print(str(len(r)/5*100)+"%")
    r.append(stanford_POS(sample))
    print(str(len(r)/5*100)+"%")
    r.append(treetagger_POS(sample))
    print(str(len(r)/5*100)+"%")
    r.append(RNNtagger_POS(sample))
    print(str(len(r)/5*100)+"%")
    r.append(talismane_POS(sample))
    pr.disable()
    
    #then print the initial sentence and the tags of each algorithm
    print(str(len(r)/5*100)+"%")
    print("FTB\t\t",sample)
    print("spacy\t\t", r[0])
    print("stanford\t\t", r[1])
    print("treetagger\t", r[2])
    print("RNNtagger\t", r[3])
    print("talismane\t",r[4])
    if timeanalysis==True:
        pstats.Stats(pr).sort_stats("cumulative").print_stats()
    return 
    
    
def spacy_POS(sample):
    '''
    Gets a list of the tags found by Spacy of the sample.
    '''
    #first, we check if the sample is a text
    try:sample=str(sample)
    except:raise Exception('Not interpretable as a string, please change the type.')
    
    #ask the spacy module to analyse the file
    tagged = spacy_nlp(sample)
    
    #retrieve the Spacy postags and make a list out of it
    r=[]
    for token in tagged:
        r.append(token.pos_)
    return r

def stanford_POS(sample):
    '''
    Gets a list of the tags found by Stanford POStagger of the sample.
    '''
    #first, we check if the sample is a text
    try:sample=str(sample)
    except:raise Exception('Not interpretable as a string, please change the type.')
    
    #first, write the sample text in a file
    previouspath=os.popen("pwd").read()[:-1]
    f= open("testsample.txt","w+",encoding="utf8")
    f.write(sample)
    f.close()
    samplepath=previouspath+"/testsample.txt"
    
    
    #then, make sure we're in the location where the stanford tagger is installed
    os.chdir("/Users/lucas/Desktop/CodeV/stanford-postagger-full-2018-10-16")
    
    #then get the path we're in and ask stanford postagger to write the result in a specific file in this path, using the sample text already wrote down.
    path=os.popen("pwd").read()[:-1]
    resultpath=previouspath+"/result_stanford.txt"
    invoke("java -mx300m -classpath stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/french-ud.tagger -textFile "+samplepath+" > "+resultpath)
    #then get the result in python variable 'result'
    result=open(resultpath,"r",encoding="utf8")
    result_lines=result.read().split("\n")
    result.close()
    
    #processing of the result file
    result_list=[]
    for line in result_lines:
        tag=-1
        for character in line:
            if character==" ":
                #at the end of a tag, there is always a " "
                result_list.append(tag)
                tag=-1
            elif character=="_":
                #at the beginning of a tag, there is always a "_"
                tag=""
            elif tag!=-1:
                #if we're in the tag, make sure to keep the character
                tag=tag+character
        result_list.append(tag)
    
    #make sure we get back to where we were before and end the fucntion
    os.chdir(previouspath)
    return result_list[:-1]

def treetagger_POS(sample):
    '''
    Gets a list of the tags found by Treetagger of the sample.
    '''
    #first, we check if the sample is a text
    try:sample=str(sample)
    except:raise Exception('Not interpretable as a string, please change the type.')
    
    #instantiate the tagger from the wrapper
    #the tagger wasn't up to date, a modification of parameter files names has been done inside its code
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr')
    
    #then analyse the sample text with the treetagger instantiated before.
    tags = tagger.tag_text(sample)
    #processing of the result file
    result=[]
    for word in tags:
        begintag=0
        tag=""
        for character in word:
            if character=="\t" and begintag==0:
                #at the beginning of a tag, there is always a "\t"
                begintag=1
            elif character=="\t" and begintag==1:
                #at the end of a tag, there is always a "\t"
                result.append(tag)
                break
            elif begintag==1:
                #when we're in the tag, we make sure we add the characters to the result
                tag=tag+character
                
    #at last, return the result
    return result

def talismane_POS(sample):
    '''
    Gets a list of the tags found by Talismane of the sample.
    '''
    try:sample=str(sample)
    #first, we check if the sample is a text
    except:raise Exception('Not interpretable as a string, please change the type.')
    
    #keep the initial directory in memory
    previouspath=os.popen("pwd").read()[:-1]
    
    #write down the sample in a .txt file and register its path
    f= open("testsample.txt","w+",encoding="utf8")
    f.write(sample)
    f.close()
    samplepath=previouspath+"/testsample.txt"
    
    
    #then go in the directory where talismane is installed 
    os.chdir("/Users/lucas/Desktop/CodeV/Talismane/talismane-distribution-5.2.0-bin")
    #and store it in the memory as 'path'   
    path=os.popen("pwd").read()[:-1]
    resultpath=previouspath+"/result_talismane.tal"
    #call the talismane algorthme to analyse the samplefile
    invoke("java -Xmx1G -jar -Dconfig.file=talismane-fr-ud-output-5.2.0.conf talismane-core-5.2.0.jar --encoding=UTF8 --inFile="+samplepath+" --outFile="+resultpath+" --analyse --endModule=posTagger --sessionId=fr")
    
    os.chdir(previouspath)
    #store the result in the python variable 'result'
    result=open("result_talismane.tal","r",encoding="utf8")
    result_lines=result.read().split("\n")
    result.close()
    
    #process the result to keep the tags only
    r=[]
    for line in result_lines[:-2]:
        if line!='':
            line=line.split()
            try:
                r.append(line[3])
            except:print(line)
    
    
    #make sure we get back to where we were before theis function call
    
    return r



#des changements conséquents ont été effectués sur les fichiers de RNNtager pour pouvoir faire fonctionner.
def RNNtagger_POS(sample):
    '''
    Gets a list of the tags found by RNNTagger of the sample.
    /!\ DOESN'T WORK /!\
    '''
    #first, we check if the sample is a text
    try:sample=str(sample)
    except:raise Exception('Not interpretable as a string, please change the type.')
    
    previouspath=os.popen("pwd").read()[:-1]
    f= open("testsample.txt","w+",encoding="utf8")
    f.write(sample)
    f.close()
    samplepath=previouspath+"/testsample.txt"
    
    

    os.chdir("/Users/lucas/Desktop/CodeV/RNNTagger")
    path=os.popen("pwd").read()[:-1]
    resultpath=previouspath+"/result_RNNTagger.txt"
    result_lines=invoke("/Users/lucas/Desktop/CodeV/RNNTagger/cmd/rnn-tagger-french.sh "+samplepath+" > "+resultpath)
    os.chdir(previouspath)
    result=open("result_RNNTagger.txt","r")
    result_lines=result.read().split("\n")
    result.close()
    r=[]
    for line in result_lines:
        if line!='':
            #in this format, the TAG et the annotations are split with  '.'   ;In order to get the tag, we take only the 1st element of the TAG'package'
            line=line.split()[1]#lets select the TAG'package
            line=line.split(".")
            r.append(line[0])
    return r

if __name__=="__main__":
    POS_5_print("Les poules du couvent couvent.")
    

    
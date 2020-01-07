# -*- coding: utf-8 -*-
import sys
sys.path.append('/Users/lucas/Desktop/CodeV/code_Python')
import analysis_parsers as analysis
import matplotlib.pyplot as plt
import pandas as pa
import numpy as np
import os



RNNoperates=False
#######Tools
def read_csv_data(filename):
    data = pa.read_csv(filename, header=None)
    #print(data.shape)
    values = data.values
    if min(values.shape) == 1:  # This If is to make the code insensitive to column-wise or row-wise expression #
        if values.shape[0] == 1:
            values = values.tolist()
        else:
            values = values.transpose()
            values = values.tolist()
        values[0]=[0]+values[0]
        return values[0]        
    else:
        data_dict = {}
        if min(values.shape) == 1:  # For single-dimension parameters in Excel
            if values.shape[0] == 1:
                for i in range(values.shape[1]):
                    data_dict[i] = values[1][i]
            else:
                for i in range(values.shape[0]):
                    data_dict[i] = values[i][1]
            
        else:  # For two-dimension (matrix) parameters in Excel
            for i in range(values.shape[0]):
                for j in range(values.shape[1]):
                    data_dict[(i, j)] = values[i][j]
        return data_dict
#####computation of the different parsers and storage in .csv files
data=[]
def POS_FTB(file_dir):
    #prend en argument un file dir correspondant à la direction d'un fichier conll dans FTB/dependencies
    file=open(file_dir,"r", encoding="utf8")
    
    lines=file.read().split("\n")
    file.close()
    tagsFTB=[]
    traitsFTB=[]
    for line in lines:
        if line!="":
            line=line.split("\t")
            line[1]=line[1]
            tagsFTB.append(line[3])
            traitsFTB.append(line[5])
    #lecture du sample avec les espaces, propre, à partir du xml.
    new_path='/'.join(file_dir.split('/')[0:-1])
    os.chdir(new_path)
    os.chdir("../Corpustext")
    
    file=open("lmf"+file_dir.split("/")[-1][4:-6]+".xml.txt","r", encoding="utf8")
    sample=file.read()
    file.close()
    return sample,tagsFTB,traitsFTB
    
def analyse_result(file_dir):
    tags=[[],[],[],[],[],[]]
    sample,tags[0],_=POS_FTB(file_dir)
    #print(sample,tags[0])
    tags[1]=analysis.spacy_POS(sample)
    tags[2]=analysis.stanford_POS(sample)
    tags[3]=analysis.treetagger_POS(sample)
    if RNNoperates:
        tags[4]=analysis.RNNtagger_POS(sample)
    else:
        tags[4]=["RNNinoperate" for i in range(len(tags[0]))]
    tags[5]=analysis.talismane_POS(sample)
    return tags,sample

def saveanalysis(file_dir, out_dir):
    global data
    values,sample=analyse_result(file_dir)
    
    #values est un np array contenant les résultats
    maxLen=max(len(values[i]) for i in range(len(values)))
    for i in range(len(values)):
        values[i] = values[i] + [""]*(maxLen - len(values[i]))
    data=values
    values=np.array(values)
    
    
    sample =list(sample.split())
    for i in range(len(sample)):
        if sample[i]==",":sample[i]='","'
        if sample[i]==";":sample[i]='";"'
        if sample[i]==")":sample[i]='")"'
        if sample[i]=="(":sample[i]='"("'
        if sample[i]=='"':sample[i]='“'
    for tags in values:
        for i in range(len(tags)):
            if tags[i]==",":tags[i]='","'
            if tags[i]==";":tags[i]='";"'
            if tags[i]==")":tags[i]='")"'
            if tags[i]=="(":tags[i]='"("'
            if tags[i]=='"':tags[i]='“'


    sample = sample + [""]*(maxLen - len(sample))
    values=np.vstack([sample,values])
    values=np.transpose(values)
    #on convertit ce np array en csv:
    os.chdir(out_dir)

    np.savetxt(file_dir.split("/")[-1]+"_result.csv",values, delimiter=",", encoding="utf8", fmt='%s')


#########interpretation of quantities
def repartitiontags(tag_list):
    tags={}
    for tag_entity in tag_list:
        tag_entity=list(tag_entity.split(":"))[0]
        if tag_entity not in tags.keys():
            tags[tag_entity]=1
        else:
            tags[tag_entity]+=1
    return tags
def savequantities(file_dir, out_dir):
    tags,_=analyse_result(file_dir)
    data=[]
    tagger_name_repartition,tagger_count_repartition=[],[]
    for tag_list in tags:
        dic_repartition=repartitiontags(tag_list)
        tagger_name_repartition,tagger_count_repartition=[],[]
        for name in dic_repartition.keys():
            tagger_name_repartition.append(name)
        tagger_name_repartition.sort()
        tagger_count_repartition=[dic_repartition[name] for name in tagger_name_repartition]
        data.append(tagger_name_repartition)
        data.append(tagger_count_repartition)
    maxlen=max(len(line) for line in data)
    for i in range(len(data)):
        line=data[i]
        data[i]=line+[""]*(maxlen-len(line))
    data=np.array(data)
    
    data=np.transpose(data)
    os.chdir(out_dir)
    np.savetxt(file_dir.split("/")[-1]+"_repartition.csv",data, delimiter=",", encoding="utf8", fmt='%s')

################generalisation to the whole French TreeBank
def analyse_folder(in_folder,out_folder):
    os.chdir(out_folder)
    os.mkdir("raw_analysis")
    os.mkdir("statistics")
    os.chdir(in_folder)
    
    listfiles=os.listdir()
    for file in listfiles:
        print(listfiles.index(file)/len(listfiles))
        if file.split(".")[-1]=="conll":
            saveanalysis(in_folder+"/"+file,out_folder+"/raw_analysis")
            savequantities(in_folder+"/"+file,out_folder+"/statistics")


def analyse_folder_summary(out_folder):
    os.chdir(out_folder+"/statistics")
    files=os.listdir(out_folder+"/statistics")
    data = pa.read_csv(files[0], header=None)
    result_array=[[0 for j in range(data.shape[1])] for i in range(data.shape[0])]
    for file in files:
        data=read_csv_data(file)
        try:
            for key in data.keys():
                value=data[key]
                if type(value)==int:
                    result_array[key[0]][key[1]]+=value
                elif type(value)==str:
                    result_array[key[0]][key[1]]=value
        except:
            print(file)
    print(result_array)
    np.savetxt(out_folder+"/corpus_result_summary.csv",result_array, delimiter=",", encoding="utf8", fmt='%s')

def addlist(initlist, listtoadd):
    #change the lists in initlist and append the ones in listtoadd
    for i in range(len(initlist)):
        initlist[i]+=listtoadd[i]

def repartition_folder_summary(in_folder,out_folder):
    os.chdir(in_folder)
    
    listfiles=os.listdir()
    data=[]
    total_tag_result=[[] for i in range(6)]
    for file in listfiles:
        print(int(listfiles.index(file)/len(listfiles)*100),"  %")
        if file.split(".")[-1]=="conll":
            file_dir=in_folder+"/"+file
            tag_result,_=analyse_result(file_dir)
            addlist(total_tag_result, tag_result)
            
    tagger_name_repartition,tagger_count_repartition=[],[]
    for tag_list in total_tag_result:
        dic_repartition=repartitiontags(tag_list)
        tagger_name_repartition,tagger_count_repartition=[],[]
        for name in dic_repartition.keys():
            tagger_name_repartition.append(name)
        tagger_name_repartition.sort()
        tagger_count_repartition=[dic_repartition[name] for name in tagger_name_repartition]
        data.append(tagger_name_repartition)
        data.append(tagger_count_repartition)
    maxlen=max(len(line) for line in data)
    for i in range(len(data)):
        line=data[i]
        data[i]=line+[""]*(maxlen-len(line))
    data=np.array(data)
    
    data=np.transpose(data)
    os.chdir(out_folder)
    np.savetxt("corpus_repartition.csv",data, delimiter=",", encoding="utf8", fmt='%s')

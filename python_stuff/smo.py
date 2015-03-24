# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 23:57:51 2015

@author: Epoch
"""

import csv
import os
import numpy as np
import pandas as pd
import scipy as sc
from numpy import genfromtxt

def uniqueFun(seq): 
   # order preserving function extracting unique elements from sequence
   checked = []
   for e in seq:
       if e not in checked:
           checked.append(e)
   return checked

def createDict(n, k) : 
    k = 1 #for now
    stage = {}
    stage['stage2'] = ([1, 2], [1, 3], [2, 1])
    print "the n is ", n
    for i in range(3, n+1):
        nameLast = "stage{0}".format(i-1)
        nameNow = "stage{0}".format(i)
        for j in range(0, len(stage[nameLast])):
            last = stage[nameLast][j][-1]
            slast = stage[nameLast][j][-2]
            # stage is i
            # node in stage is j
            print "Stage no. ", i 
            print "Node no. ", j
            if i<n :
                if last < i:
                    if j==0: # if its the first record in this stage
                        stage[nameNow]=([slast, last, i], )
                        tempList = list(stage[nameNow])      
                        tempList.append([slast, last, i+k])
                    else :
                        tempList.append([slast, last, i])
                        tempList.append([slast, last, i+1])
                elif last==i :
                    tempList.append([slast, last, i-1])
                # elis last>i another elif here if we go beyond the k=1 case
            elif i==n :
                lastN = list(set([i-1, i]).difference([last, slast]))
                lastN = int(''.join(map(str,lastN))) #turning to integer
                lastNode = [slast, last, lastN]
                #print(lastNode)
                if j==0 :
                    stage[nameNow]=([lastNode],)
                    tempList = list(stage[nameNow])
                else:  
                    tempList.append(lastNode)
                    
        stage[nameNow]=tuple(tempList)


    newStage={}
    newStage['stage2'] = ([1, 2], [1, 3], [2, 1])
    newStage['stage1'] = ([1], [2])
    # now to clean the network for unique elements
    for i in range(3, n+1): 
        nameNow = "stage{0}".format(i)
        newStage[nameNow] = tuple(uniqueFun(stage[nameNow]))
        
    return newStage
                                        
 myDic = createDict(10, 1)                                   


def createDict2(n, k) : 
    k = 1 #for now
    stage = {}
    arcSet = {}
    stage['stage2'] = ([1, 2], [1, 3], [2, 1])
    print "the n is ", n
    for i in range(3, n+1):
        nameLast = "stage{0}".format(i-1)
        nameNow = "stage{0}".format(i)
        for j in range(0, len(stage[nameLast])):
            last = stage[nameLast][j][-1]
            slast = stage[nameLast][j][-2]
            # stage is i
            # node in stage is j
            print "Stage no. ", i 
            print "Node no. ", j
            if i<n :
                if last < i:
                    if j==0: # if its the first record in this stage
                        stage[nameNow]=([slast, last, i], )
                        tempList = list(stage[nameNow])      
                        tempList.append([slast, last, i+k])
                    else :
                        tempList.append([slast, last, i])
                        tempList.append([slast, last, i+1])
                elif last==i :
                    tempList.append([slast, last, i-1])
                # elis last>i another elif here if we go beyond the k=1 case
            elif i==n :
                lastN = list(set([i-1, i]).difference([last, slast]))
                lastN = int(''.join(map(str,lastN)))
                lastNode = [slast, last, lastN]
                #print(lastNode)
                if j==0 :
                    stage[nameNow]=([lastNode],)
                    tempList = list(stage[nameNow])
                else:  
                    tempList.append(lastNode)
                    
        stage[nameNow]=tuple(tempList)


    newStage={}
    newStage['stage2'] = ([1, 2], [1, 3], [2, 1])
    newStage['stage1'] = ([1], [2])
    # now to clean the network for unique elements
    for i in range(3, n+1): 
        nameNow = "stage{0}".format(i)
        newStage[nameNow] = tuple(uniqueFun(stage[nameNow]))
    arcSet['1to2'] = 
    for (i in range(0, n-1)):
        
        
    return newStage
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 06 13:10:54 2015

@author: Epoch
"""

import os
import nltk.data
from nltk.tokenize import WordPunctTokenizer, wordpunct_tokenize
import pandas as pd
import nltk
import re, codecs
from __future__ import division
from nltk.stem.snowball import SnowballStemmer
import numpy as np
from datetime import datetime, timedelta
# a naive and incomplete demonstration on how to read a *.spydata file
import pickle
import tarfile
import pbr
import lda
import itertools
import time
os.chdir("C:\\Users\\Epoch\\Documents\\GitHub\\scraper-project\\uni")

# open a .spydata file
filename = 'big10_data.spydata'
tar = tarfile.open(filename, "r")
# extract all pickled files to the current working directory
tar.extractall()
extracted_files = tar.getnames()
for f in extracted_files:
    if f.endswith('.pickle'):
         with open(f, 'rb') as fdesc:
             data = pickle.loads(fdesc.read())
os.chdir("C:\\Users\\Epoch\\Documents\\GitHub\\scraper-project\\documents")


dictElMundo = data["dictElMundo"]
dictExpansion = data["dictExpansion"]
dictElPais = data["dictElPais"]


def giveDTM(tokList, dictionary) :
    docArray = np.zeros((len(tokList), len(dictionary)), dtype=np.int32)
    counterDoc = 0
    for doc in tokList :
        counterTerm = 0
        for term in dictionary :
            docArray[counterDoc, counterTerm] = doc.count(term)
            counterTerm +=1
        counterDoc +=1
       #print counterDoc
    return docArray

def giveTopicsList(topic_object, n_top_words, uniqueWords) :
    #function gives list of unique n_top_words for each topic
    list_of_topics_words = []
    for i, topic_dist in enumerate(topic_object):
        topic_words = np.array(uniqueWords)[np.argsort(topic_dist)][:-n_top_words:-1]
        #topic_words = [unicode(a, "utf8") for a in topic_words]
        tempList = [a for a in topic_words]
        list_of_topics_words.append(tempList)
        #final_list = list(itertools.chain(*list_of_topics_words))
    return (list(set(list(itertools.chain(*list_of_topics_words)))))
    
def compare_lists(x, y):
     count = 0
     for num in y:
             if num in x:
                     count += 1
     return count

#### Creating reorganising into data frame by time 
pdElMundo = pd.DataFrame()
pdExpansion = pd.DataFrame()
pdElPais = pd.DataFrame()

ind1 = 0
ind2 = 0
ind3 = 0    
    
for company in dictElMundo : 
    for article in dictElMundo[company] :
        #print type(dictElMundo[company])
        tempDf = pd.DataFrame(article, index=[0])
        pdElMundo= pdElMundo.append(tempDf, ignore_index=True)
        ind1+=1
        print "adding article number %s for el mundo " % ind1
    
for company in dictElPais : 
    for article in dictElPais[company] :
        #print type(dictElMundo[company])
        tempDf = pd.DataFrame(article, index=[0])
        pdElPais = pdElPais.append(tempDf, ignore_index=True)
        ind2+=1
        print "adding article number %s for el pais " %ind2
        
for company in dictExpansion : 
    for article in dictExpansion[company] :
        #print type(dictElMundo[company])
        tempDf = pd.DataFrame(article, index=[0])
        pdExpansion = pdExpansion.append(tempDf, ignore_index=True)
        ind3+=1
        print "adding article number %s for expansion " % ind3
        
allArticles = pd.concat([pdExpansion, pdElPais, pdElPais], ignore_index=True)
realDate = [datetime.strptime(a, "%d/%m/%Y") for a in allArticles["fecha"]]
allArticles["date"] = pd.DataFrame(realDate)

"""
relevantArticles = allArticles[allArticles["date"]>datetime.strptime("01/06/2014", "%d/%m/%Y")]
relNews = relevantArticles.sort(["date"], ascending=[1])
relNews1 = relNews.drop_duplicates(cols="link", take_last=True)
text =  relNews1["texto"].head(100)

rawText = RawDocs_spanish(text, "stopWEsp.txt")
rawText.token_clean(2)
rawText.stopword_remove()
cleanTokens = rawText.tokens

allCorpus = []
for a in cleanTokens :
    allCorpus +=a
    

          

uniqueWords = list(set(allCorpus))

DTM = giveDTM(cleanTokens, uniqueWords)
if_idf_dict = rawText.if_idf(uniqueWords)
if_idf_mat = np.array(pd.DataFrame(if_idf_dict), dtype=np.int32)

model_if = lda.LDA(n_topics=20, n_iter=1500, random_state=1)
model = lda.LDA(n_topics=20, n_iter=1500, random_state=1)

model.fit(DTM)
model_if.fit(if_idf_mat.T)

topic_word_if = model_if.topic_word_
topic_word = model.topic_word_


n_top_words = 8
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(uniqueWords)[np.argsort(topic_dist)][:-n_top_words:-1]
    #topic_words = [unicode(a, "utf8") for a in topic_words]
    temp = [a.encode("utf8") for a in topic_words]
    topics = 'Topic {}: {}'.format(i, ' '.join(temp))
    print topics

for topic_dist in enumerate(topic_word_if):
    topic_words_if = np.array(uniqueWords)[np.argsort(topic_dist)][:-n_top_words:-1]
    #topic_words = [unicode(a, "utf8") for a in topic_words]
    temp = [a for a in topic_words_if]
    #topics = 'Topic {}: {}'.format(i, ' '.join(temp))
    print temp
    
"""


    
    
model_if = lda.LDA(n_topics=20, n_iter=1500, random_state=1)
model = lda.LDA(n_topics=20, n_iter=1500, random_state=1)

window = 2 # months
n_top_words = 8
frequency_re_estim = 14
initial_window = datetime(2014, 8, 1) - datetime(2014, 8-window, 1)
current_date = datetime(2014, 8, 7)

indicator_count = []
indicator_if_idf = []

list_of_topics_count = []
list_of_topics_if_idf = []

ind = 0

while current_date < datetime(2015, 6, 1) :
    
    start_date = current_date - timedelta(window*30)
    
    relevantArticles = allArticles[allArticles["date"]>=start_date]
    relevantArticles = relevantArticles[relevantArticles["date"]<=current_date]
    
    print "... got relevant articles...%s" % time.ctime()
    
    relNews = relevantArticles.sort(["date"], ascending=[1])
    relNews1 = relNews.drop_duplicates(cols="link", take_last=True)
    text =  relNews1["texto"]
    
    rawText = RawDocs_spanish(text, "stopWEsp.txt")
    rawText.token_clean(2)
    rawText.stopword_remove()
    rawText.stem()
    cleanStems = rawText.stems
    
    print "... got clean tokens...%s" % time.ctime()
    
    allCorpus = []
    for a in cleanStems :
        allCorpus +=a
    uniqueWords = list(set(allCorpus))
    
    print "... creating epic matrices...%s" % time.ctime()  
    
    DTM = giveDTM(cleanStems, uniqueWords)
    if_idf_dict = rawText.if_idf(uniqueWords)
    if_idf_mat = np.array(pd.DataFrame(if_idf_dict), dtype=np.int32)
    
    model.fit(DTM)
    model_if.fit(if_idf_mat.T)
    
    print "... fitting topic model... %s" % time.ctime()

    topic_word_if = model_if.topic_word_
    topic_word = model.topic_word_
    
    print "... fit the models, about to count some magic...%s" % time.ctime()
    
    topics_count = giveTopicsList(topic_word, n_top_words, uniqueWords)
    topics_if_idf = giveTopicsList(topic_word_if, n_top_words, uniqueWords)
    
    list_of_topics_count.append(topics_count)
    list_of_topics_if_idf.append(topics_if_idf)
    
    print "... counted the magic, about to create indicator... %s" % time.ctime()
    
    if ind > 0:
        count_same_terms = compare_lists(list_of_topics_count[-1], list_of_topics_count[-2])
        if_idf_same_terms = compare_lists(list_of_topics_if_idf[-1], list_of_topics_if_idf[-2])        
        
        #effectively measures similarity between two periods
        indicator_count.append(count_same_terms/len(list_of_topics_count[-1]))
        indicator_if_idf.append(if_idf_same_terms/len(list_of_topics_if_idf[-1]))
    ind +=1
    current_date  + timedelta(frequency_re_estim)
    print "... done for this date, next date starts at %s" % current_date
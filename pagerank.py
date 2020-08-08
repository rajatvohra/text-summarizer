import nltk
import pandas as pd
import numpy as np
from urllib import request
from nltk import *
import math
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from bs4 import BeautifulSoup as bs
import re
from boilerpy3 import extractors
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx


#nltk.download('punkt')
#nltk.download('stopwords')
#download above 2 first

stop_words=set(stopwords.words('english')) 

#####trying ends rn rh ###############



url ="https://timesofindia.indiatimes.com/pcpaathshala/parents/parents-articles/managing-stress-in-the-new-normal/Intelshow/76957466.cms"
url="https://timesofindia.indiatimes.com/entertainment/hindi/bollywood/news/maharashtra-government-files-sushant-singh-rajput-probe-report-in-sc-hearing-on-aug-11/articleshow/77432744.cms"
def get_data_bs(url):
  html = urllib.request.urlopen(url).read()
  soup =bs(html,'html.parser')
  cont=soup.findAll('p')
  content=''
  for para in cont:
    content+=para.text

  cleaned_content=re.sub(r'\[[0-9]*\]',' ',content)
  cleaned_content_final=re.sub(r'\s+',' ',cleaned_content)
  return cleaned_content_final

def get_data_b4(url):
    
  extractor = extractors.ArticleExtractor()
  content = extractor.get_content_from_url(url)
  cleaned_content=re.sub(r'\[[0-9]*\]',' ',content)
  cleaned_content_final=re.sub(r'\s+',' ',cleaned_content)
  return cleaned_content_final

#####trying ends rn rh ###############


def sent_tokenizing(file):
  sentences=nltk.sent_tokenize(file)
  return sentences

def similiarity_bw_sents(s1,s2,stop_words):
  s1=[s.lower() for s in s1]
  s2=[s.lower() for s in s2]

  all_words=list(set(s1+s2))
  first_vec=[0]*len(all_words)
  second_vec=[0]*len(all_words)

  for word in s1:
    if word in stop_words:
      continue
    first_vec[all_words.index(word)]+=1

  for word in s2:
    if word in stop_words:
      continue
    second_vec[all_words.index(word)]+=1

  return 1- cosine_distance(first_vec,second_vec)

def sentence_similiarity_matrix(sentences,stop_words):
  matrix=np.zeros((len(sentences),len(sentences)))
  for i in range(len(sentences)):
    for j in range(len(sentences)):
      if(i!=j):
        matrix[i][j]=similiarity_bw_sents(sentences[i],sentences[j],stop_words)
  return matrix

def sentences_ranked(matrix,sentences):
  graph=nx.from_numpy_array(matrix)
  ranks=nx.pagerank(graph)
  ranks_sorted=sorted(((ranks[i],s) for i,s in enumerate(sentences)), reverse=True)  
  return ranks_sorted


def get_summary(sorted_sents,lines):
  summary=""
  for i in range(lines):
    summary+=sorted_sents[i][1]
    summary+='\n'
  return summary

def headline(sorted_sents):
  return get_summary(sorted_sents,1)
  
def main():
  url=input("enter the url\n")
  type_=input("headline or summary?\n")
  content=get_data_b4(url)

  sentences=sent_tokenizing(content)

  matrix=sentence_similiarity_matrix(sentences,stop_words)
  sorted_sents=sentences_ranked(matrix,sentences)
  if(type_.lower()=='headline'):
    print(headline(sorted_sents))
  else:
    tn=int(input("n for top-n sentences"))
    print(get_summary(sorted_sents,tn))


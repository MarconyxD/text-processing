# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 21:53:20 2021

@author: Marcony Montini
"""

from glob import glob
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def parsetexts(fileglob='C:/Users/Marcony Montini/Desktop/Tarefa 1/Arquivos/pf*.htm'):
    texts, words = {}, set()
    for txtfile in glob(fileglob): # loop para ler cada um dos arquivos dentro da pasta
        with open(txtfile, encoding='latin1') as f:
            txt = f.read() # leitura do arquivo e salvando como uma string
            
            # sequência de tratamentos para retirar termos e caracteres que atrapalhariam
            text = txt[txt.find('</P>'):]
            text = re.sub('<P>A', '', text) # remove toda inicialização do narrador A
            text = re.sub('<P>X', '', text) # remove toda inicialização do narrador X
            cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});') 
            text = re.sub(cleanr, '', text) # remove tags html
            text = re.sub(r'[^a-zA-Z ]', '', text) # remove símbolos
            text = re.sub('tilde', '', text) # remove erro devido uso de ~
            text = re.sub('acute', '', text) # remove erro devido uso de ´
            text = re.sub('grave', '', text) # remove erro devido uso de `
            text = re.sub('cedil', '', text) # remove erro devido uso de ç
            
            # conversão da string para list para criar os índices
            txt = text # para passar de strpara lista basta só colocar .split() na frente
            
            words |= set(txt)
            texts[txtfile.split('\\')[-1]] = txt
    return texts, words


docs, words = parsetexts()

texts = []
nomesDocs = []

# Convertendo o dictionary para duas lists: nomesDocs e texts
for key, value in docs.items():
    temp = [key,value]
    nomesDocs.append(temp[0])
    texts.append(temp[1])

search_terms = "pois"

# Modelo vetorial
doc_vectors = TfidfVectorizer().fit_transform([search_terms] + texts)

# Criando ranking em uma variável documents_scores
cosine_similarities = linear_kernel(doc_vectors[0:1], doc_vectors).flatten()
document_scores = [item.item() for item in cosine_similarities[1:]]

# Juntando os nomes dos docs e os scores em um dictionary e depois em um dataframe
resultado = {'nomesDocs':nomesDocs,'scores':document_scores}

resultado = pd.DataFrame(resultado)

# Imprimindo os 10 melhores resultados em ordem decrescente
print('\nRanking dos 10 textos com maior score para a busca de termos realizada: ')
print(resultado.sort_values('scores', ascending=False).head(10))


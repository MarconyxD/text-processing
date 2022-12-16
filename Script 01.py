# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 15:46:56 2021

@author: Marcony Montini
"""

import re
import os
import nltk
import matplotlib.pyplot as plt
from collections import Counter
from glob import iglob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')

#print(stopwords.words('portuguese'))

def removerLixo(text):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});') 
    text = re.sub(cleanr, '', text) # remove tags html
    text = re.sub(r'\b\w\b', ' ', text) # remove uma letra sobrando
    text = re.sub(r'[^a-zA-Z ]', '', text) # remove símbolos
    text = re.sub('tilde', '', text) # remove erro devido uso de ~
    text = re.sub('acute', '', text) # remove erro devido uso de ´
    text = re.sub('grave', '', text) # remove erro devido uso de `
    text = text.lower() # coloca tudo em letra minúscula
    text_tokens = word_tokenize(text)
    text = [word for word in text_tokens if not word in stopwords.words()] # stopwords
    return text

topwords = 10
folderpath = 'C:/Users/Marcony Montini/Desktop/Tarefa 1/Arquivos/pf*.htm'
counter = Counter()
contador = 0

# Loop que abre cada um dos arquivos, remove o lixo e salva no Counter as palavras e ocorrências
for filepath in iglob(os.path.join(folderpath, '*.htm')):
    print(int((contador/143)*100),"%") # Imprime porcentagem com base nos 143 arquivos na pasta
    contador += 1
    with open(filepath, encoding='latin1') as file:
        counter.update(removerLixo(file.read()))
        #counter.update(removerLixo(file.read()).split()) para aplicar sem stopwords

# Loop que imprime as palavras mais comuns e número de ocorrências
for word, count in counter.most_common(topwords):
    print('{}: {}'.format(count, word))

# Variáveis auxiliares para pegar apenas as mais comuns e plotar
maisComuns = counter.most_common(topwords)
palavra = [x[0] for x in maisComuns]
quantidade = [x[1] for x in maisComuns]

# Salvar imagem do plot e plotar
plt.bar(palavra, quantidade, 1)
plt.savefig('plot.png')
plt.show()
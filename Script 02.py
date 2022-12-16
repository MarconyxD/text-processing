# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 15:46:13 2021

@author: Marcony Montini
"""
from pprint import pprint as pp
from glob import glob
from functools import reduce
import re
import nltk
import pickle
nltk.download('stopwords')
nltk.download('punkt')

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
            txt = text.split()
            
            words |= set(txt)
            texts[txtfile.split('\\')[-1]] = txt
    return texts, words
 
def termsearch(terms): # busca por índice invertido
    return reduce(set.intersection,
                  (invindex[term] for term in terms),
                  set(texts.keys()))

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


texts, words = parsetexts()
print('\nTextos')
pp(texts)
print('\nPalavras')
pp(sorted(words))

# impressão do índice com todos os termos e nome do texto que possui ocorrência
invindex = {word:set(txt
                     for txt, wrds in texts.items() if word in wrds)
            for word in words}
    
print('\nÍndice Invertido')
pp({k:sorted(v) for k,v in invindex.items()})

save_obj(invindex,"Indice")
save_obj(texts,"texts")
    

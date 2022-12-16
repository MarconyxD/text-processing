# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 14:35:43 2021

@author: Marcony Montini
"""

from collections import defaultdict
from glob import glob
from copy import deepcopy
from math import log
import re


# ## Importar os dados e criar o índice inverso

def import_dataset():
    """
    Função apra importação de todos os documentos e tratamento dos dados
    """
    fileglob='C:/Users/Marcony Montini/Desktop/Tarefa 1/Arquivos/pf*.htm'
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
            
            apenastextos = []
            
            for key, value in texts.items():
                temp = [key,value]
                apenastextos.append(temp[1])
    return apenastextos

# ### Função para pegar apenas os nomes dos documentos

def pega_titulos(fileglob='C:/Users/Marcony Montini/Desktop/Tarefa 1/Arquivos/pf*.htm'):
    texts = {}
    for txtfile in glob(fileglob): # loop para ler cada um dos arquivos dentro da pasta
        with open(txtfile, encoding='latin1') as f:
            txt = f.read() # leitura do arquivo e salvando como uma string
            texts[txtfile.split('\\')[-1]] = txt
    return texts


def make_inverted_index(corpus):
    """
    Função para criar o índice inverso
    """
    index = defaultdict(set)
    for docid, article in enumerate(corpus):
        for term in article:
            index[term].add(docid)
    return index


# ### União de duas listas


def posting_lists_union(pl1, pl2):
        """
        Retorna uma nova lista de postagens resultante da união das duas listas 
        passadas como argumentos.
        """
        pl1 = sorted(list(pl1))
        pl2 = sorted(list(pl2))
        union = []
        i = 0
        j = 0
        while (i < len(pl1) and j < len(pl2)):
            if (pl1[i] == pl2[j]):
                union.append(pl1[i])
                i += 1
                j += 1
            elif (pl1[i] < pl2[j]):
                union.append(pl1[i])
                i += 1
            else:
                union.append(pl2[j])
                j += 1
        for k in range(i, len(pl1)):
            union.append(pl1[k])
        for k in range(j, len(pl2)):
            union.append(pl2[k])
        return union


# ## Precomputing weights


def DF(term, index):
    '''
    Função de computação da freqüência do documento para um termo.
    '''
    return len(index[term])


def IDF(term, index, corpus):
    '''
    Função que calcula a frequência inversa do documento para um termo.
    '''
    return log(len(corpus)/DF(term, index))


def RSV_weights(corpus,index):
    '''
    Esta função calcula previamente os pesos do Valor do Status de Recuperação 
    para cada termo no índice
    '''
    N = len(corpus)
    w = {}
    for term in index.keys():
        p = DF(term, index)/(N+0.5)  
        w[term] = IDF(term, index, corpus) + log(p/(1-p))
    return w
    


# ## BIM Class


class BIM():
    '''
    Classe de modelo de independência binária
    '''
    
    def __init__(self, corpus):
        self.original_corpus = deepcopy(corpus)
        self.articles = corpus
        self.index = make_inverted_index(self.articles)
        self.weights = RSV_weights(self.articles, self.index)
        self.ranked = []
        self.query_text = ''
        self.N_retrieved = 0
    
    
        
    def RSV_doc_query(self, doc_id, query):
        '''
        Esta função calcula o valor do status de recuperação para um determinado 
        documento - consulta usando os pesos pré-calculados

        '''
        score = 0
        doc = self.articles[doc_id]
        for term in doc:
            if term in query:
                score += self.weights[term]     
        return score

    
        
    def ranking(self, query):
        '''
        Função auxiliar para a função answer_query. Calcula a pontuação apenas 
        para documentos que estão na lista de postagem de pelo menos um termo 
        na consulta
        '''

        docs = []
        for term in self.index: 
            if term in query:
                docs = posting_lists_union(docs, self.index[term])
                
        scores = []
        for doc in docs:
            scores.append((doc, self.RSV_doc_query(doc, query)))
        
        self.ranked = sorted(scores, key=lambda x: x[1], reverse = True)
        return self.ranked
    
    
    
    def recompute_weights(self, relevant_idx, query):
        '''
        Função auxiliar para a função relevância_feedback e para o feedback de 
        pseudo relevância na função answer_query. Recomputa os pesos, apenas 
        para os termos na consulta com base em um conjunto de documentos relevantes.
        '''
        
        relevant_docs = []
        for idx in relevant_idx:
            doc_id = self.ranked[idx-1][0]
            relevant_docs.append(self.articles[doc_id])
        
        N = len(self.articles)
        N_rel = len(relevant_idx)
        
        for term in query:
            if term in self.weights.keys():
                vri = 0
                for doc in relevant_docs:
                    if term in doc:
                        vri += 1
                p = (vri + 0.5) /( N_rel + 1)
                u = (DF(term, self.index) - vri + 0.5) / (N - N_rel +1)
                self.weights[term] = log((1-u)/u) + log(p/(1-p))

            
    
    def answer_query(self, query_text):
        '''
        Função para responder a uma consulta de texto livre. Mostra as primeiras 
        30 palavras dos 15 documentos mais relevantes. Também implementa o 
        feedback de pseudo relevância com k = 5
        '''
        
        self.query_text = query_text
        query =  query_text.upper().split()
        ranking = self.ranking(query)
        
        ## pseudo relevance feedback 
        i = 0
        new_ranking=[]
        while i<10 and ranking != new_ranking:
            self.recompute_weights([1,2,3,4,5], query)
            new_ranking = self.ranking(query)
            i+=1
        
        ranking = new_ranking
        
        self.N_retrieved = 15
        
        ## print retrieved documents
        
        for i in range(0, self.N_retrieved):
            article = self.original_corpus[ranking[i][0]]
            if (len(article) > 30):
                article = article[0:30]
        self.weights = RSV_weights(self.articles, self.index)


            
    def relevance_feedback(self, *args):
        '''
        Função que implementa feedback de relevância para a última consulta 
        formulada. O conjunto de documentos relevantes é fornecido pelo usuário 
        por meio de um conjunto de índices

        '''
        if(self.query_text == ''):
            print('Não é possível obter feedback antes de uma consulta ser formulada.')
            return
        
        relevant_idx = list(args)
        
        if(isinstance(relevant_idx[0], list)):
            relevant_idx = relevant_idx[0]
        
        query = self.query_text.upper().split()
        self.recompute_weights(relevant_idx,query)
        
        self.answer_query(self.query_text)


# Example of usage

articles = import_dataset()
bim  = BIM(articles)
search_terms = "pois"
bim.answer_query(search_terms)

docs = pega_titulos()

nomesDocs = []

# Passando os nomes dos documentos para nomesDocs
for key, value in docs.items():
    temp = [key,value]
    nomesDocs.append(temp[0])

aux = 0;
for listaRanking in bim.ranked:
    tituloDocumento = nomesDocs[listaRanking[0]]
    scoreDocumento = listaRanking[1]
    print("Documento: ", tituloDocumento, "     Score: ", scoreDocumento)
    aux += 1
    if aux == 10: break

   
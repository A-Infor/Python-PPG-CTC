# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 16:32:42 2024

Esse programa:  coleta SPEI de todos os anos da planilha,
                executa os cálculos subsequentes p/ todos os anos.
"""

import os
os.chdir('E:\POSCOMP\Códigos e datasets do Sandro')
###IMPORTAÇÕES#################################################################
import pandas            as pd
import numpy             as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
###############################################################################
def preencher_dados_ano_a_ano(dados_gabi, dados_ano_a_ano):
    col_num = 1
    
    for ano in range(ANO_INICIAL,ANO_FINAL):
        dados_ano_a_ano[ano] = dados_gabi.iloc[:, col_num]
        dados_ano_a_ano[ano] = dados_ano_a_ano[ano].values.reshape(-1, 1)
        print ("ano: ", ano, ", col_num: ", col_num)
        col_num+=1
    return dados_ano_a_ano

def criar_clusteres_ano_a_ano(dados_ano_a_ano):
    resultados   = {} # um  dicionário
    
    for ano in range(ANO_INICIAL,ANO_FINAL):
        inercias     = [] # uma lista
        n_cidades    = dados_ano_a_ano[ano].shape[0]
        print("ano: ", ano, ", num. cidades: ", n_cidades)
        
        for n_clusters in np.arange(1, n_cidades):
            print("ano: ", ano, ", cluster num.: ", n_clusters)
            kmeans = KMeans(n_clusters = n_clusters, n_init = 10)
            kmeans.fit(dados_ano_a_ano[ano])
            inercias.append(kmeans.inertia_)
        
        print("ano:", ano, ", inercias: ", len(inercias))
        resultados[ano] = inercias
        
    return resultados

def reduz_num_clusteres(dados_ano_a_ano):
    n_clusters = 8
    
    for ano in range(ANO_INICIAL,ANO_FINAL):
        kmeans         = KMeans(n_clusters=n_clusters, n_init = 10)
        cluster_labels = kmeans.fit_predict(dados_ano_a_ano[ano])
        print("Clusteres designados para o ano", ano, ":", cluster_labels)
        
        dados_ano_a_ano[ano] = np.column_stack((dados_ano_a_ano[ano], cluster_labels))
        
###GRÁFICOS####################################################################
def plotar_graficos_cotovelos(dados_ano_a_ano, inercias):
    
    for ano in range(ANO_INICIAL,ANO_FINAL):
        n_cidades    = dados_ano_a_ano[ano].shape[0]
        
        plt.figure(figsize=(8, 6))
        plt.plot(np.arange(1, n_cidades), inercias[ano], '-o')
        
        plt.xlabel('Numero de clusteres')
        plt.ylabel('Inertia')
        plt.title('Ano: ' + str(ano))
        
def plotar_graficos_clusteres(dados_ano_a_ano):
    for ano in range(ANO_INICIAL,ANO_FINAL):
        dados_ano_a_ano[ano].plot(kind='scatter', x='Valor', y='Cluster', s=32, alpha=.8)
        plt.gca().spines[['top', 'right',]].set_visible(False)
        plt.title('Ano: ' + str(ano))
    
        
###"MAIN"######################################################################
dados_gabi      = pd.read_excel('dados_GabrielaTCC.xlsx', sheet_name="spei")
dados_ano_a_ano = {}
ANO_INICIAL     = 2003
ANO_FINAL       = 2020

dados_ano_a_ano = preencher_dados_ano_a_ano(dados_gabi, dados_ano_a_ano)
inercias        = criar_clusteres_ano_a_ano(dados_ano_a_ano)

plotar_graficos_cotovelos(dados_ano_a_ano, inercias)

reduz_num_clusteres(dados_ano_a_ano)

for ano in range(ANO_INICIAL,ANO_FINAL):
    dados_ano_a_ano[ano] = pd.DataFrame(dados_ano_a_ano[ano], columns=['Valor', 'Cluster'])        

plotar_graficos_clusteres(dados_ano_a_ano)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
*  Trabalho 1: BUSCA HEURÍSTICA E BUSCA LOCAL
*  INF1771 - INTELIGÊNCIA ARTIFICIAL
* 
*  Autores: Luiz Arthur Meira - 1512570
*
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import time
import math
import copy
import random
import numpy as np
from Interface import Interface

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
* PARAMETROS GLOBAIS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 574

ETAPAS = ['0','1','2','3','4','5','6','7','8','9','B','C','D','E','G','H','I','J','K','L','N','O','P','Q','S','T','U','V','W','X','Y','Z']

AGILIDADE = [1.8,1.6,1.6,1.6,1.4,0.9,0.7]

TEMPO = {
  ".": 1,
  "R": 5,
  "F": 10,
  "A": 15,
  "M": 200
}

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
* CRIAÇÃO DE MAPA
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def create_map(file):
    arq = open(file,'r')
    aux = arq.readlines()
    map = []
    for linha in aux:
        if list(linha)[-1] == '\n':
            map.append(list(linha[0:-1]))
        else:
            map.append(list(linha))
    return map

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
*  BUSCA A*
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def find_stage(mapa, stage):
    etapa = ETAPAS[stage]
    for x in range(len(mapa)):
        for y in range(len(mapa[i])):
            elem = mapa[x][y]
            if elem == etapa:
                return [x,y]

def get_neighbors(map, position):
    neighbors = []
    if position[0] > 0:
        neighbors.append([position[0]-1,position[1]])
    if position[1] < len(map[0])-1:
        neighbors.append([position[0],position[1]+1])
    if position[0] < len(map)-1:
        neighbors.append([position[0]+1,position[1]])
    if position[1] > 0:
        neighbors.append([position[0],position[1]-1])
    return neighbors

def get_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) #Distância de Manhattan

def find_path_step(map, step, interface, custos):
    inicio = find_stage(map, step)
    final = find_stage(map, step+1)
    visitados = [inicio]
    caminho = [[0 for col in range(len(map[0]))] for row in range(len(map))]
    caminho[inicio[0]][inicio[1]] = ['s', 0]
    melhorCaminho = [final]
    while final not in visitados:
        min = 1000000000
        current = [-1,-1] # Ponto que sera utilizado para alcancar o vizinho
        proximoVizinho = [-1,-1] # Vizinho
        remove = [] 
        for ponto in visitados:
            neighbors = get_neighbors(map, ponto)
            if neighbors == []:
                remove.append(ponto)
            else:
                valido = 0 
                for vizinho in neighbors:
                    if caminho[vizinho[0]][vizinho[1]] == 0: # Ainda não foi visitado
                        valido = 1
                        if map[vizinho[0]][vizinho[1]] in ['.', 'R', 'F', 'A', 'M']: # Vizinho é igual a alguma superficie válida
                            value = caminho[ponto[0]][ponto[1]][1] + TEMPO[map[vizinho[0]][vizinho[1]]] + get_distance(vizinho, final)
                            if value < min:
                                min = value
                                proximoVizinho = vizinho
                                current = ponto
                        else:
                            value = caminho[ponto[0]][ponto[1]][1] + get_distance(vizinho, final)
                            if value < min:
                                min = value
                                proximoVizinho = vizinho
                                current = ponto
                if valido == 0:
                    remove.append(ponto)
        for ponto in remove:
            visitados.remove(ponto)
        value = min - get_distance(proximoVizinho, final)
        visitados.append(proximoVizinho)
        caminho[proximoVizinho[0]][proximoVizinho[1]] = [[current[0]-proximoVizinho[0],current[1]-proximoVizinho[1]],value] 
    while inicio not in melhorCaminho: 
        interface.update(caminho,melhorCaminho,step,custos)
        ant = caminho[melhorCaminho[0][0]][melhorCaminho[0][1]][0] 
        melhorCaminho.insert(0,[melhorCaminho[0][0]+ant[0],melhorCaminho[0][1]+ant[1]])
    interface.update([[0 for col in range(len(map[0]))] for row in range(len(map))],melhorCaminho,step,custos)
    custo = caminho[final[0]][final[1]][1] 
    return melhorCaminho, custo

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
*  SIMULATED ANNEALING
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def get_random_array(agilidades):
    array = [[0 for col in range(31)] for row in range(7)]
    for i in range(7):
        aux = []
        while len(aux) < 8:
            indice = random.randint(0,30)
            if indice not in aux:
                array[i][indice] = 1
                aux.append(indice)
    min = agilidades[0]
    min_index = 0
    for i, val in enumerate(agilidades):
        if val < min:
            min = val
            min_index = i
    i = 0
    while True:
        if array[min_index][i] == 1:
            break
        i += 1
    array[min_index][i] = 0
    return array

def update_array(array, max, atual):
    aux = copy.deepcopy(array)
    n = math.ceil(atual/(max/32))
    num = random.randint(1,n)
    for i in range(num):
        i = random.randint(0,6)
        j = random.randint(0,30)
        if aux[i][j] == 0:
            aux[i][j] = 1
            k = random.randint(0,30)
            while k == j or aux[i][k] == 0:
                k = random.randint(0,30)
            aux[i][k] = 0
        else:
            aux[i][j] = 0
            k = random.randint(0,30)
            while k == j or aux[i][k] == 1:
                k = random.randint(0,30)
            aux[i][k] = 1
    return aux

def objective(array, etapas, agilidades):
    total = 0
    for j in range(31):
        soma = 0
        for i in range(7):
            soma += array[i][j] * agilidades[i]
        if soma == 0:
            soma = 0.00001
        total += etapas[j]/soma
    return total


def Simulated_annealing(etapas, agilidades, temp, interface):
    n_iterations = 100000 # Numero de passos em um Simulated Annealing
    for k in range(4):
        best = get_random_array(agilidades)
        best_val = objective(best,etapas,agilidades)
        if k == 0:
            melhor = best_val
            melhor_val = copy.deepcopy(best)
        curr = copy.deepcopy(best)
        curr_val = best_val
        scores = []
        scores.append(best_val)
        for i in range(n_iterations):
            t = temp / ((i/100)+1) # calculate temperature for current epoch
            candidate = update_array(curr, temp, t) 
            candidate_val = objective(candidate, etapas, agilidades)
            if candidate_val < best_val:
                best = candidate
                best_val = candidate_val
                scores.append(best_val)
            diff = candidate_val - curr_val # difference between candidate and current point evaluation
            metropolis = np.exp(-diff / t) # calculate metropolis acceptance criterion
            if diff < 0 or random.uniform(0, 1) < metropolis: # check if we should keep the new point
                curr, curr_val = candidate, candidate_val # store the new current point
        if best_val < melhor:
            melhor = best_val
            melhor_val = copy.deepcopy(best)  
    return melhor_val, melhor

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
* MAIN
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    
etapas = []
for i in range(31):
    etapas.append((i+1)*10)

interface = Interface(SCREEN_WIDTH,SCREEN_HEIGHT)

map = create_map('mapa.txt')
interface.add_map(map)
path = []
custos = []
for i in range(31):
    caminho, custo = find_path_step(map,i,interface,custos)
    path.append(caminho)
    custos.append(custo)
interface.finish(path)
best, best_val = Simulated_annealing(etapas,AGILIDADE,800,interface)
interface.update_finish(best, custos, best_val)

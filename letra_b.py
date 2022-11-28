from helpers import *
from matplotlib import pyplot as plt
from matplotlib import cm
from typing import Callable, Tuple
import math
import random
import numpy as np


def funcao(input: Tuple[float, float]) -> float:
    x = input[0]
    y = input[1]
    soma = x**2 + y**2
    num = (math.sin(math.sqrt(soma)))**2 - 0.5
    den = (1 + 0.001*soma)**2
    return 0.5 - num / den


def funcao_np(x: np.ndarray, y: np.ndarray):
    soma = x**2 + y**2
    num = np.sin(np.sqrt(soma))**2 - 0.5
    den = (1 + 0.001*soma)**2
    return 0.5 - num / den


x_minimo = -100
x_maximo = 100
quantidade = 1000
numero_de_geracoes = 1000
prob_cruzamento = 0.9
prob_mutacao = 0.2


def plotar(nome: str, avaliacoes: list[float], melhores_xy: list[Tuple[float, float]]):
    geracoes = [i + 1 for i in range(numero_de_geracoes)]
    x = [v[0] for v in melhores_xy]
    y = [v[1] for v in melhores_xy]

    plt.figure()
    ax = plt.subplot(1, 2, 1)
    ax.plot(geracoes, avaliacoes, 'r--')
    ax.set_xlim(1, numero_de_geracoes)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Gerações')
    ax.set_ylabel('Fitness')
    ax.set_title('Evolução do AG')
    ax.grid('on')

    ax = plt.subplot(1, 2, 2)
    ax.scatter(x, y)
    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
    ax.set_xlabel('X')
    ax.set_title('Pontos avaliados')
    ax.grid('on')

    plt.savefig(f'fig/{nome}.png', bbox_inches='tight')


def cruzamento(povo: list[Tuple[float, float]], indices: list[int]) -> list[Tuple[float, float]]:
    for i in range(math.floor(len(indices) / 2)):
        pai_1 = povo[2*i]
        pai_2 = povo[2*i+1]
        if random.random() < prob_cruzamento:
            alfa = random.random()
            yield interpolar_tupla(pai_1, pai_2, alfa)
            yield interpolar_tupla(pai_1, pai_2, 1-alfa)
        else:
            yield pai_1 + tuple()
            yield pai_2 + tuple()


desvio = x_maximo / math.sqrt(6)


def mutacao(povo: list[Tuple[float, float]], probm: float) -> None:
    for i in range(0, len(povo)):
        if random.random() <= probm:
            povo[i] = (povo[i][0] + random.gauss(0, desvio), povo[i][1])
        if random.random() <= probm:
            povo[i] = (povo[i][0], random.gauss(0, desvio) + povo[i][1])


def entrada_rand() -> Tuple[float, float]:
    x = float(random.randrange(x_minimo, x_maximo))
    y = float(random.randrange(x_minimo, x_maximo))
    return (x, y)


def main(nome: str, funcao_selecao: Callable[[list[Tuple[float, float]]], list[int]]):
    povo = [entrada_rand() for _ in range(quantidade)]
    avaliacoes = []

    melhores_xy: list[Tuple[float, float]] = []
    melhores_aval: list[float] = []

    for i in range(numero_de_geracoes):
        avaliacoes = [funcao(v) for v in povo]
        soma_avals = sum(avaliacoes)
        avals_rels = [x / soma_avals for x in avaliacoes]
        indices = funcao_selecao(avals_rels)
        cruzados = list(cruzamento(povo, indices))
        mutacao(cruzados, prob_mutacao)

        # Elitismo
        avaliacoes_finais = [funcao(v) for v in cruzados]
        aval_pior_inicial = min(avaliacoes)
        aval_melhor_final = max(avaliacoes_finais)
        if aval_melhor_final > aval_pior_inicial:
            index_velho = avaliacoes.index(aval_pior_inicial)
            index_novo = avaliacoes_finais.index(aval_melhor_final)
            povo[index_velho] = cruzados[index_novo]
            avaliacoes[index_velho] = aval_melhor_final

        melhor_aval = max(avaliacoes)
        melhores_aval.append(melhor_aval)
        melhores_xy.append(povo[avaliacoes.index(melhor_aval)])

    print(max(melhores_aval))
    plotar(nome, melhores_aval, melhores_xy)


main('b-roleta', selecao_roleta)
main('b-torneio', selecao_torneio)

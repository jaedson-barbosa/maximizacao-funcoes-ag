from helpers import *
from matplotlib import pyplot as plt
from typing import Callable
import math
import random


def funcao(x: float) -> float: return 1/((x-3)**2+0.1)+1/((x-2)**2+0.05)+2


x_minimo = -2
x_maximo = 8
quantidade = 10
numero_de_geracoes = 100
n_bits = 15
prob_cruzamento = 0.8
prob_mutacao = 0.05


def plotar(nome: str, avaliacoes: list[float], melhores_x: list[float]):
    geracoes = [i + 1 for i in range(numero_de_geracoes)]
    x_referencia = [x / 100 for x in range(x_minimo * 100, x_maximo * 100 + 1)]
    y_referencia = [funcao(x) for x in x_referencia]
    y_m_solucoes = [funcao(x) for x in melhores_x]

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
    ax.plot(x_referencia, y_referencia, 'r--', melhores_x, y_m_solucoes, 'b.')
    ax.set_xlabel('x')
    ax.set_title('Y calculado')
    ax.grid('on')

    plt.savefig(f'fig/{nome}.png', bbox_inches='tight')


def cruzamento(bits_povo: list[list[int]], indices: list[int]) -> list[list[int]]:
    for i in range(math.floor(len(indices) / 2)):
        pai_1 = bits_povo[2*i]
        pai_2 = bits_povo[2*i+1]
        if random.random() < prob_cruzamento:
            alfa = random.randint(1, n_bits-1)
            yield pai_1[0:alfa+1] + pai_2[alfa+1:]
            yield pai_2[0:alfa+1] + pai_1[alfa+1:]
        else:
            yield pai_1.copy()
            yield pai_2.copy()


def mutacao(bits_habitantes: list[list[int]], probm: float) -> None:
    for i in range(0, len(bits_habitantes)):
        for j in range(0, n_bits):
            if random.random() <= probm:
                v = bits_habitantes[i][j]
                bits_habitantes[i][j] = 1 if v == 0 else 0


def main(nome: str, funcao_selecao: Callable[[list[float]], list[int]]):
    rnds = [int(random.randrange(2**n_bits)) for _ in range(quantidade)]
    bits_povo = [bytes_to_bitarray(number, n_bits) for number in rnds]
    nums_povo = [normalize_number(x, n_bits, x_minimo, x_maximo) for x in rnds]

    avaliacoes = []
    melhores_x = []
    melhores_aval = []

    for i in range(numero_de_geracoes):
        avaliacoes = [funcao(v) for v in nums_povo]
        soma_avals = sum(avaliacoes)
        avals_rels = [x / soma_avals for x in avaliacoes]
        indices = funcao_selecao(avals_rels)
        cruzados = list(cruzamento(bits_povo, indices))
        mutacao(cruzados, prob_mutacao)

        # Elitismo
        nums = [bits_to_number(v) for v in cruzados]
        nums = [normalize_number(v, n_bits, x_minimo, x_maximo) for v in nums]
        avaliacoes_finais = [funcao(v) for v in nums]
        aval_pior_inicial = min(avaliacoes)
        aval_melhor_final = max(avaliacoes_finais)
        if aval_melhor_final > aval_pior_inicial:
            index_velho = avaliacoes.index(aval_pior_inicial)
            index_novo = avaliacoes_finais.index(aval_melhor_final)
            bits_povo[index_velho] = cruzados[index_novo]
            nums_povo[index_velho] = nums[index_novo]
            avaliacoes[index_velho] = aval_melhor_final

        melhor_aval = max(avaliacoes)
        melhores_aval.append(melhor_aval)
        melhores_x.append(nums_povo[avaliacoes.index(melhor_aval)])

    print(max(melhores_aval))
    plotar(nome, melhores_aval, melhores_x)


main('a-roleta', selecao_roleta)
main('a-torneio', selecao_torneio)

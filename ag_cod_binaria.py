from math import ceil, floor
from ag import Populacao, Selecao
from matplotlib import pyplot as plt
from typing import Callable


def main(nome: str, selecao: Selecao, x_minimo: float, x_maximo: float, fitness: Callable[[float], float], avaliacao: Callable[[float], float], numero_de_geracoes: int):
    quantidade = 50
    n_bits = 15
    probabilidade_cruzamento = 0.8
    probabilidade_mutacao = 0.05

    index_geracao = []
    avaliacoes = []
    melhores_x = []

    populacao = Populacao(quantidade, n_bits, x_minimo,
                          x_maximo, selecao, avaliacao)

    for i in range(numero_de_geracoes):
        populacao.geracao(probabilidade_cruzamento, probabilidade_mutacao)
        avals = populacao.avaliacoes
        melhor_aval = max(avals)
        avaliacoes.append(melhor_aval)
        index_geracao.append(i)
        index_melhor_sol = avals.index(melhor_aval)
        melhor_x = populacao.nums_habitantes[index_melhor_sol]
        melhores_x.append(melhor_x)

    x_referencia = [x / 100 for x in range(x_minimo * 100, x_maximo * 100 + 1)]
    y_referencia = [fitness(x) for x in x_referencia]
    y_m_solucoes = [fitness(x) for x in melhores_x]

    plt.figure()
    plt.subplot(1, 2, 1)
    plt.plot(index_geracao, avaliacoes, 'r--')
    plt.xlim((0, numero_de_geracoes))
    plt.yscale('log')
    plt.xlabel('Gerações')
    plt.ylabel('Fitness')
    plt.title('Evolução do AG')
    plt.grid('on')

    plt.subplot(1, 2, 2)
    plt.plot(x_referencia, y_referencia, 'r--', melhores_x, y_m_solucoes, 'b.')
    plt.xlabel('x')
    plt.title('Y calculado')
    plt.grid('on')

    plt.savefig(f'fig/{nome}.png', bbox_inches='tight')

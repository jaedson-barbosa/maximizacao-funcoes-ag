import random
import numpy as np
from enum import Enum
from typing import Callable
from helpers import *
import math
from itertools import accumulate, count


class Selecao(Enum):
    ROLETA = 0
    TORNEIO = 1


class Populacao:
    def __init__(self, quantidade: int, n_bits: int, min: float, max: float, selecao: Selecao, avaliacao: Callable[[float], float]):
        self.quantidade = quantidade
        self.n_bits = n_bits
        self.min = min
        self.max = max
        root_numbers = [int(random.randrange(2**n_bits))
                        for _ in range(quantidade)]
        bits = [bytes_to_bitarray(number, n_bits) for number in root_numbers]
        numbers = [self.normalize_number(x) for x in root_numbers]
        avaliacoes = [avaliacao(v) for v in numbers]
        self.bits_habitantes = bits
        self.nums_habitantes = numbers
        self.avaliacao = avaliacao
        self.avaliacoes = avaliacoes
        self.selecao = selecao

    def normalize_number(self, number: int) -> float:
        return self.min + number*(self.max-self.min)/(2**self.n_bits - 1)

    def bits_to_number(self, bits: list[int]):
        return self.normalize_number(bits_to_number(bits))

    def get_fitness_relativo(self):
        fitness = [self.avaliacao(v) for v in self.nums_habitantes]
        soma_fitness = sum(fitness)
        return [x / soma_fitness for x in fitness]

    def __selecao_roleta(self) -> list[int]:
        probs = self.get_fitness_relativo()
        rnds = [random.random() for _ in range(self.quantidade)]
        prob_ac = list(accumulate(probs))
        c_index = [len(list(filter(lambda x: x > v, prob_ac))) for v in rnds]
        return [self.quantidade - v for v in c_index]

    def __selecao_torneio(self, probc: float):
        probs = self.get_fitness_relativo()
        rnds = [random.random() for _ in range(self.quantidade)]
        return list(filter(lambda i: rnds[i] < probc, range(self.quantidade)))

    def __cruzamento(self, indices: list[int], probc: float) -> list[list[int]]:
        end_range = math.floor(len(indices) / 2)
        resultado = [[0]] * end_range * 2
        for i in range(0, end_range):
            r = random.random()
            pai_1 = self.bits_habitantes[2*i]
            pai_2 = self.bits_habitantes[2*i+1]
            if r <= probc:
                alfa = random.randint(1, self.n_bits-1)
                resultado[2*i] = pai_1[0:alfa+1] + pai_2[alfa+1:]
                resultado[2*i+1] = pai_2[0:alfa+1] + pai_1[alfa+1:]
            else:
                resultado[2*i] = pai_1.copy()
                resultado[2*i+1] = pai_2.copy()
        return resultado

    def __mutacao(self, bits_habitantes: list[list[int]], probm: float) -> None:
        for i in range(0, len(bits_habitantes)):
            for j in range(0, self.n_bits):
                r = random.random()  # Geração de um número aleatorio
                if r <= probm:  # Se o numero aleatorio for menor do que probm então se realiza a mutação
                    v = bits_habitantes[i][j]
                    bits_habitantes[i][j] = 1 if v == 0 else 0

    def __apply_elitismo(self, bits_habitantes: list[list[int]]):
        nums_finais = [self.bits_to_number(v) for v in bits_habitantes]
        avaliacoes_finais = [self.avaliacao(v) for v in nums_finais]
        avaliacao_pior_inicial = min(self.avaliacoes)
        avaliacao_melhor_final = max(avaliacoes_finais)
        if avaliacao_melhor_final > avaliacao_pior_inicial:
            index_pior_inicial = self.avaliacoes.index(avaliacao_pior_inicial)
            index_melhor_final = avaliacoes_finais.index(
                avaliacao_melhor_final)
            bits_melhor_final = bits_habitantes[index_melhor_final]
            nums_melhor_final = self.bits_to_number(bits_melhor_final)
            self.bits_habitantes[index_pior_inicial] = bits_melhor_final
            self.nums_habitantes[index_pior_inicial] = nums_melhor_final
            self.avaliacoes[index_pior_inicial] = avaliacao_melhor_final

    def geracao(self, probc: float, probm: float):
        indices_selecionados = self.__selecao_roleta(
        ) if self.selecao == Selecao.ROLETA else self.__selecao_torneio(probc)
        if self.selecao == Selecao.TORNEIO:
            probc = 1
        habitantes_cruzados = self.__cruzamento(indices_selecionados, probc)
        self.__mutacao(habitantes_cruzados, probm)
        self.__apply_elitismo(habitantes_cruzados)

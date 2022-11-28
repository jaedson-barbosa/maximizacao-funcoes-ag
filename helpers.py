from functools import reduce
from itertools import accumulate
from typing import Tuple
import random


def bits_to_number(bits: list[int]):
    return reduce(lambda a, b: a * 2 + b, bits)


def bytes_to_bitarray(number: int, n_bits: int):
    bits = bin(number)[2:]
    padded_bits = '0'*(n_bits-len(bits)) + bits
    bits_array = [1 if bit == '1' else 0 for bit in padded_bits]
    return bits_array


def normalize_number(number: int, n_bits: int, min: float, max: float) -> float:
    return min + number*(max-min)/(2**n_bits - 1)


def selecao_roleta(avaliacoes: list[float]) -> list[int]:
    quantidade = len(avaliacoes)
    prob_ac = list(accumulate(avaliacoes))
    rnds = [random.random() for _ in range(quantidade)]
    c_index = [len(list(filter(lambda x: x > v, prob_ac))) for v in rnds]
    result = [quantidade - v for v in c_index]
    return result


def selecao_torneio(lst):
    l = len(lst)
    return [i if lst[i] > lst[i+1] else i+1 for i in range(0, l, 2)]


def interpolar_tupla(tuplaA: Tuple[float, float], tuplaB: Tuple[float, float], alpha: float):
    x = tuplaA[0] * alpha + tuplaB[0] * (1-alpha)
    y = tuplaA[1] * alpha + tuplaB[1] * (1-alpha)
    return (x, y)

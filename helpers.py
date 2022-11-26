from functools import reduce


def bits_to_number(bits: list[int]):
    return reduce(lambda a, b: a * 2 + b, bits)


def bytes_to_bitarray(number: int, n_bits: int):
    bits = bin(number)[2:]
    padded_bits = '0'*(n_bits-len(bits)) + bits
    bits_array = [1 if bit == '1' else 0 for bit in padded_bits]
    return bits_array

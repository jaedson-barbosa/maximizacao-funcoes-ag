import ag


def test_bits_to_number():
    assert ag.bits_to_number([1, 1, 1]) == 7
    assert ag.bits_to_number([1, 0, 0, 0, 0, 0, 0, 0]) == 128


def test_bytes_to_bitarray():
    assert ag.bytes_to_bitarray(255, 8) == [1, 1, 1, 1, 1, 1, 1, 1]
    assert ag.bytes_to_bitarray(256, 9) == [1, 0, 0, 0, 0, 0, 0, 0, 0]

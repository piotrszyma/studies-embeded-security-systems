import unittest
import functools
import random

DEFAULT_FILENAME = '/tmp/a51_output.txt'


class VhdlTestCase(unittest.TestCase):
  @functools.lru_cache()
  def read_output_bits(self, filename=DEFAULT_FILENAME):
    with open(filename, 'r') as bits_file:
      return [int(bit.strip()) for bit in bits_file.readlines()]

  def get_random_bits(self, amount=100):
    return [int(bit) for bit in bin(random.getrandbits(amount))[2:]]

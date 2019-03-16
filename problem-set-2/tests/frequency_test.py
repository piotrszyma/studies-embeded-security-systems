import math
import unittest
import logging

from scipy import special as scipy_special

import testing_lib


def _full_chunks(bits, chunk_size):
  """Chunks bits iterable into chunk_size sequences."""
  for idx in range(len(bits) // chunk_size):
    chunk = bits[idx * chunk_size:idx * chunk_size + chunk_size]
    if len(chunk) != chunk_size:
      return
    yield chunk


def _ones_to_all_proportion(block):
  return sum(block) / len(block)


def _equal_pairs(block):
  return sum(0 if block[idx] == block[idx + 1] else 1
             for idx, _ in enumerate(block[:-1])) + 1


class A51Tests(testing_lib.VhdlTestCase):
  def test_frequency_monobit(self):
    """Test 1"""
    bits = self.read_output_bits()
    sum_of_normalized_bits = sum(2 * bit - 1 for bit in bits)
    s_obs = abs(sum_of_normalized_bits) / math.sqrt(len(bits))
    p_value = scipy_special.erfc(s_obs / math.sqrt(2))
    logging.info('S_n = %s', sum_of_normalized_bits)
    logging.info('S_obs = %s', s_obs)
    logging.info('P_value = %s', p_value)
    assert p_value >= 0.01

  def test_frequency_within_a_block(self):
    """Test 2"""
    bits = self.read_output_bits()
    chunk_size = 3
    blocks = list(_full_chunks(bits, chunk_size))
    blocks_proportions = [_ones_to_all_proportion(block) for block in blocks]
    x_squared = 4 * chunk_size * sum(
        (proportion - 0.5)**2 for proportion in blocks_proportions)
    p_value = 1 - scipy_special.gammainc(len(blocks) / 2, x_squared / 2)
    logging.info('P_value = %s', p_value)
    assert p_value >= 0.01

  def test_runs(self):
    """Test 3"""
    bits = self.read_output_bits()
    len_of_bits = len(bits)
    pi = _ones_to_all_proportion(bits)
    v_n = _equal_pairs(bits)
    p_value = 1 - scipy_special.erf(
        (abs(v_n - 2 * len_of_bits * pi *
             (1 - pi))) / (2 * math.sqrt(2 * len_of_bits) * pi * (1 - pi)))
    logging.info('v_n = %s', v_n)
    logging.info('p_n = %s', p_value)
    assert p_value >= 0.01


if __name__ == '__main__':
  logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(message)s")
  unittest.main()

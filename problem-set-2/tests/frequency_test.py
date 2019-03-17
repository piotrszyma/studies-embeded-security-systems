import math
import unittest
import logging
import collections
import operator

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


def _get_counts_of_groups_of_ones(blocks, groups_sizes):
  """Returns array of number of occurences of specific group

  Returns:
    [num_of_v0, num_of_v1, ..., num_of_vn]
  """
  normalized_min_size = min(groups_sizes)
  normalized_max_size = max(groups_sizes)
  normalized_chunks = collections.defaultdict(int)
  for group_size in groups_sizes:
    normalized_chunks[group_size] = 0

  for block in blocks:
    max_size = max(len(chunk)
                   for chunk in ''.join(str(bit) for bit in block).split('0')
                   if chunk)
    if max_size <= normalized_min_size:
      normalized_chunks[normalized_min_size] += 1
    elif max_size >= normalized_max_size:
      normalized_chunks[normalized_min_size] += 1
    else:
      normalized_chunks[max_size] += 1
  return [
    count for _, count in sorted(normalized_chunks.items(),
    key=operator.itemgetter(0))]

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
    # bits = self.read_output_bits()
    bits = self.get_random_bits()
    len_of_bits = len(bits)
    pi = _ones_to_all_proportion(bits)
    v_n = _equal_pairs(bits)
    p_value = 1 - scipy_special.erf(
        (abs(v_n - 2 * len_of_bits * pi *
             (1 - pi))) / (2 * math.sqrt(2 * len_of_bits) * pi * (1 - pi)))
    logging.info('v_n = %s', v_n)
    logging.info('p_n = %s', p_value)
    assert p_value >= 0.01

  def test_longest_run_of_ones_in_a_block(self):
    """Test 4"""
    bits = self.get_random_bits(amount=7000)
    len_of_bits = len(bits)
    assert 6272 < len_of_bits < 750_000
    chunk_size = 128
    blocks = list(_full_chunks(bits, chunk_size))
    v = _get_counts_of_groups_of_ones(blocks, [4, 5, 6, 7, 8, 9])
    K = len(v) - 1
    assert K == 5 # Based on table, number of groups - 1
    pi = [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124] # Values from book
    N = 49 # based on len_of_bits in range and chunk_size == 128
    x_squared = sum(
      ((v_i - N * pi_i) ** 2) / (N * pi_i)  for pi_i, v_i in zip(pi, v))
    p_value = 1 - scipy_special.gammainc(K / 2, x_squared / 2)
    assert p_value >= 0.01

if __name__ == '__main__':
  logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(message)s")
  unittest.main()

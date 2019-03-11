import math
import unittest
import logging

from scipy import special as scipy_special

import testing_lib


class A51Tests(testing_lib.VhdlTestCase):
  def test_frequency_monobit(self):
    bits = self.read_output_bits()
    sum_of_normalized_bits = sum(2 * bit - 1 for bit in bits)
    s_obs = abs(sum_of_normalized_bits) / math.sqrt(len(bits))
    p_value = scipy_special.erfc(s_obs / math.sqrt(2))
    logging.info('S_n = %s', sum_of_normalized_bits)
    logging.info('S_obs = %s', s_obs)
    logging.info('P_value = %s', p_value)
    assert p_value >= 0.01


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
  unittest.main()

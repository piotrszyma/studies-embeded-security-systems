import functools
import operator
import random
import collections


def get_specific_indexes(iterable, indexes):
  return [
      value for index, value in enumerate(iterable)
      if index in frozenset(indexes)
  ]


def shift_and_calc_last(iterable, xored_indexes):
  return [
      *iterable[:-1],
      functools.reduce(operator.xor,
                       get_specific_indexes(iterable, xored_indexes))
  ]


class A51:
  def __init__(self, seed):
    assert len(seed) == 64
    self.lsfr1 = seed[:19]
    self.lsfr2 = seed[19:-23]
    self.lsfr3 = seed[-23:]

  def shift_lsfrs(self):
    self.lsfr1 = shift_and_calc_last(self.lsfr1, [18, 17, 16, 13])
    self.lsfr2 = shift_and_calc_last(self.lsfr2, [21, 20])
    self.lsfr3 = shift_and_calc_last(self.lsfr3, [22, 21, 20, 7])

  def calc_random(self):
    voting_bits = self.lsfr1[8], self.lsfr2[10], self.lsfr3[10]
    majority_bit = max(set(voting_bits), key=voting_bits.count)
    return functools.reduce(
        lambda prev, curr: prev ^ curr if curr == majority_bit else prev,
        (self.lsfr1[-1], self.lsfr2[-1], self.lsfr3[-1])
    )
    # return self.lsfr1[-1] ^ self.lsfr2[-1] ^ self.lsfr3[-1]

  def __iter__(self):
    return self

  def __next__(self):
    self.shift_lsfrs()
    return self.calc_random()


def main():
  # seed = [random.randrange(0, 2) for _ in range(23)]
  # seed = [int(bit) for bit in '00011111110111110010100']
  seed = [int(bit) for bit in '1' * 64]
  a51 = A51(seed)
  for random_number, _ in zip(a51, range(20)):
    print(random_number)


if __name__ == "__main__":
  main()

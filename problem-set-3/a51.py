import functools
import operator
import random
import collections


class A51:
  def __init__(self, seed):
    assert len(seed) == 64
    self.lsfr1 = seed[:19]
    self.lsfr2 = seed[19:-23]
    self.lsfr3 = seed[-23:]

  def shift_lsfrs(self):
    voting_bits = self.lsfr1[8], self.lsfr2[10], self.lsfr3[10]
    majority_bit = max(set(voting_bits), key=voting_bits.count)
    if self.lsfr1[8] == majority_bit:
      self.lsfr1 = [
        self.lsfr1[18] ^ self.lsfr1[17] ^ self.lsfr1[16] ^ self.lsfr1[13],
        *self.lsfr1[:-1]
      ]
    if self.lsfr2[10] == majority_bit:
      self.lsfr2 = [self.lsfr2[21] ^ self.lsfr2[20], *self.lsfr2[:-1]]
    if self.lsfr3[10] == majority_bit:
      self.lsfr3 = [
        self.lsfr3[22] ^ self.lsfr3[21] ^ self.lsfr3[20] ^ self.lsfr3[7],
        *self.lsfr3[:-1]
      ]

  def __iter__(self):
    return self

  def __next__(self):
    self.shift_lsfrs()
    return self.lsfr1[-1] ^ self.lsfr2[-1] ^ self.lsfr3[-1]


def main():
  # seed = [random.randrange(0, 2) for _ in range(23)]
  # seed = [int(bit) for bit in '00011111110111110010100']
  seed = [int(bit) for bit in '1' * 64]
  a51 = A51(seed)
  print([(random_number) for random_number, _ in zip(a51, range(40))])


if __name__ == "__main__":
  main()

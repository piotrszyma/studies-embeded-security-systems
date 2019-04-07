import pdb
from collections import Counter

class LFSR:

    def __init__(self, IV: list, voting_bit_position: int,
                 xoring_bits: list):
        self.bits = IV
        self.voting_bit_position = voting_bit_position
        self.xoring_bits = xoring_bits

    def state(self):
        return self.bits

    def out(self):
        return int(self.bits[len(self.bits)-1])

    def vote(self):
        return self.bits[self.voting_bit_position]

    def shift(self):

        x = len(self.bits)
        self.bits[1:x] = self.bits[0:x-1]

        R = int(self.bits[self.xoring_bits[0]])
        for bit in self.xoring_bits[1:]:
            R ^= int(self.bits[bit])
        self.bits[0] = str(R)

    def __repr__(self):
        return f"LSFR {len(self.bits)}"



class A5_1:

    def __init__(self, IV: list):
        xoring_bits_1 = [13, 16, 17, 18]
        xoring_bits_2 = [20, 21]
        xoring_bits_3 = [7, 20, 21, 22]

        self.lfsr_1 = LFSR(IV[:19], 8, xoring_bits_1)
        self.lfsr_2 = LFSR(IV[19:-23], 10, xoring_bits_2)
        self.lfsr_3 = LFSR(IV[-23:], 10, xoring_bits_3)


    def out(self):
        """
        Return xored bits on 0 position of each LFSR.
        """
        return self.lfsr_1.out() ^ self.lfsr_2.out() ^ self.lfsr_3.out()

    def shift(self):
        majority_bit = self.majority_voting()

        if majority_bit == self.lfsr_1.vote():
            self.lfsr_1.shift()

        if majority_bit == self.lfsr_2.vote():
            self.lfsr_2.shift()

        if majority_bit == self.lfsr_3.vote():
            self.lfsr_3.shift()

    def majority_voting(self):
        """
        Count the votes and return most common one.
        """
        votes = [self.lfsr_1.vote(), self.lfsr_2.vote(), self.lfsr_3.vote()]
        return Counter(votes).most_common(1)[0][0]

    def __iter__(self):
        return self

    def __next__(self):
        self.shift()
        return self.out()

    def get_state(self):
        return self.lfsr_1.state() + self.lfsr_2.state() + self.lfsr_3.state()



def main():
    # a = '0001111111011111001' # 19
    # b = '0001111111011111001010' # 22
    # c = '00011111110111110010100' # 23
    # IV = list(a + b + c)
    IV = list('1' * 64)
    a5_1 = A5_1(IV)
    limit = [1] * 20
    for number, _ in zip(a5_1, limit):
        print(number)


if __name__ == "__main__":
    main()
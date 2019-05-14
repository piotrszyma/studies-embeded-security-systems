import base64
import hashlib
from itertools import permutations

hash = 'fee44f690b2d81480f0c628f6105b05a'
version = '0.891.1'
pin = '5789'

def get_hash(word):
  return  hashlib.md5(word).hexdigest()

# import pdb; pdb.set_trace()

# with open('google-10000-english-no-swears.txt', 'r') as words_file:
#   for word in words_file:
#     word = word.strip()
#     hashed_word = hashlib.md5(word).hexdigest()
#     assert hashed_word != hash

letters = version + pin

for perm in permutations(letters):
  pos_hash = get_hash(''.join(perm))
  assert pos_hash != hash, ''.join(perm)

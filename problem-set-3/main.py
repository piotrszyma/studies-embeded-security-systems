import random
import argparse
import time

import serial

from a51 import A51

IV_SIZE = 20
PORT_NAME = '/dev/tty.usbserial-1410'

# Slave
# Channel 5 - read
# Channel 3 - write

# Channel 10 - RX
# Channel 11 - TX

def get_random_iv(size):
  return [random.randint(0, 1) for _ in range(size)]


def master():
  """Master actions:

  Sends IV using cable.

  Waits.

  XORs message.

  Sends message.

  """
  print('MASTER')
  with serial.Serial(PORT_NAME, 9600, timeout=1) as ser:
    print("sending otp..")
    time.sleep(0.5)
    ser.write(b'OTP1')
    time.sleep(0.5)

    ser.write(b'OTP2')
    time.sleep(0.5)

    ser.write(b'OTP3')
    time.sleep(0.5)

    import pdb; pdb.set_trace()
    print("sent otp..")

  # ser = serial.Serial()
  # ser.baudrate = 9600
  # ser.port = PORT_NAME
  # ser.open()
  # print(ser.name)
  # print("seding otp..")
  # x = ser.write(b'OTP')
  # import pdb; pdb.set_trace()
  # print('sent..')
  # time.sleep(1)
  # print("seding msg..")
  # ser.write(b'MSG')
  # print("msg sent..")
  # ser.close()


def slave():
  """Slave actions:

  Waits for IV from master using cable.

  Receives message.

  XORs IV with receives.
  """
  print('SLAVE')
  with serial.Serial(PORT_NAME, 9600) as arduino_usb:
    while True:
      print(arduino_usb.readline())
  arduino_usb.close()             # close port

def main(args):
  if args.slave:
    slave()
  else:
    master()

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--slave', action='store_true', default=False)
  args = parser.parse_args()
  main(args)

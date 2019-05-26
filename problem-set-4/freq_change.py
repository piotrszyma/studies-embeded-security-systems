"""Changing frequency."""
import time

import serial

def send(connection, data):
  print(f'Sending {data}.')
  connection.write(data)
  time.sleep(0.5)
  response = connection.readlines()
  print(f'Got response: {response}')
  time.sleep(0.5)


def main():
  with serial.Serial('/dev/cu.usbserial-142210', 9600, timeout=1) as connection:

    for _ in range(2):
      connection.write(b'aaa')
      connection.read(28)

    send(connection, b'5789')  # Enter the pin.
    send(connection, b'c 1234')  # Set new frequency.
    send(connection, b'0.891.1Wojtek\n')  # Send password.
    send(connection, b'd')  # Check new frequency.

if __name__ == "__main__":
  main()
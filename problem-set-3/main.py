import random
import argparse
import time

import serial

import a51

# ==================
# MASTER:

# Diode:
# port 5

# IR sender:
# port 6

# Cable connection:
# TX (transmit):
# port 11

# RX (receive):
# port 10
# ==================

DEFAULT_PORT = '/dev/cu.usbserial-1420'
IV_SIZE = 64

class logging:

  @staticmethod
  def info(text):
    print(text)

def get_random_iv(size):
  return ''.join([str(random.randint(0, 1)) for _ in range(size)])

def _xor_message(message_bytes, prng):
  otp_bytes = [int(''.join(str(next(prng)) for _ in range(8)), base=2) for _ in message_bytes]
  return bytes(char ^ otp_element for char, otp_element in zip(message_bytes, otp_bytes))


def encrypt_message(message_bytes, prng):
  return _xor_message(message_bytes, prng)

def decrypt_message(message_bytes, prng):
  return _xor_message(message_bytes, prng)


def send_message(message_str, cable_serial, prng):
  encrypted_message = encrypt_message(message_str.encode('utf-8'), prng)
  for counter, message_byte in enumerate(encrypted_message, start=1):
    time.sleep(0.25)
    cable_serial.write(bytes((counter, message_byte,)))
  cable_serial.write(bytes((255, 255,)))


def master(port):
  """Master actions:

  Sends IV using cable.

  Waits.

  XORs message.

  Sends message.

  """
  logging.info(f'Starting master on port')
  logging.info('IV generation phase.')
  # Hardcoded for now


  with serial.Serial(port, 9600, timeout=0) as cable_serial:
    logging.info('Master generates IV.')
    iv = get_random_iv(IV_SIZE)
    iv_bytes_msg = bytes(iv + "\n", "UTF-8")
    logging.info(iv)
    logging.info('Master waits 2s...')
    time.sleep(2)
    logging.info('Master sends IV')
    cable_serial.write(iv_bytes_msg)
    time.sleep(2)
    logging.info('Master waits 2s...')
    prng = a51.A51(tuple(int(b) for b in iv))
    master_message = 'Master: message!'
    logging.info("Master sends message...")
    time.sleep(1)
    while True:
      send_message(input(), cable_serial, prng)
      # logging.info('Waiting for slave message...')
      message = read_message(cable_serial, prng)
      print(f'Slave: {message}')
    # logging.info('Master finished his work')


def read_data(cable_serial):
  while True:
    hex_letter = cable_serial.readline().strip()
    try:
      frame_bytes = int(hex_letter).to_bytes(length=2, byteorder='big')
    except (OverflowError, ValueError) as e:
      continue
    else:
      break
  frame_letter, frame_ctr = frame_bytes[1], frame_bytes[0]
  return frame_letter, frame_ctr


def read_message(cable_serial, prng):
  encrypted_msg = b''
  expected_ctr = 1
  frame_options = []
  synchronized = False
  while True:
    frame_letter, frame_ctr = read_data(cable_serial)

    if frame_ctr == 255:
      encrypted_msg += max(
          set(frame_options),
          key=frame_options.count).to_bytes(length=1, byteorder='big')
      logging.info('End of message detected once.')
      decrypted_msg = decrypt_message(encrypted_msg, prng)
      return decrypted_msg

    if not synchronized and frame_ctr != 1:
      logging.info(f'Not synchronized and ctr: {frame_ctr}, expected ctr: {expected_ctr}')
      continue

    if not synchronized:
      logging.info(f'frame_ctr: {frame_ctr}, moving into synchronized state.')
      synchronized = True
    if frame_ctr == expected_ctr:
      logging.info(f'frame_ctr: {frame_ctr} == expected_ctr, adding option for nr {frame_ctr}.')
      frame_options.append(frame_letter)
    elif frame_ctr == expected_ctr + 1:
      logging.info(f'frame_ctr: {frame_ctr} == expected_ctr + 1, evaluating, initializing new options for nr {frame_ctr}.')
      encrypted_msg += max(
        set(frame_options),
        key=frame_options.count).to_bytes(length=1, byteorder='big')
      frame_options = [frame_letter]
      expected_ctr += 1
    else: # Not current_ctr, not current_ctr + 1
      logging.info(f'Neither expected_ctr ({expected_ctr}) or expected_ctr + 1, but {frame_ctr}')
      continue


def slave(port):
  """Slave actions:

  Waits for IV from master using cable.

  Receives message.

  XORs IV with receives.
  """
  time.sleep(1)

  logging.info(f'Starting slave on port')
  logging.info('Slave waits for data')

  with serial.Serial(port, 9600, timeout=2) as cable_serial:
    cable_serial.reset_input_buffer()
    while True:
      iv = cable_serial.read(64)
      logging.info(f'Slave reiceived IV value: {iv} of len {len(iv)}')

      if len(iv) == 64 and b'\r' not in iv and b'\n' not in iv:
        cable_serial.reset_input_buffer()
        cable_serial.reset_output_buffer()
        break
    prng = a51.A51(tuple(int(b) for b in iv.decode('utf-8')))
    while True:
      message = read_message(cable_serial, prng)
      # cable_serial.reset_input_buffer()
      # cable_serial.reset_output_buffer()
      logging.info(f'Master: {message}')
      # logging.info('Slave waits 2 second... because he can...')
      # time.sleep(2)
      # logging.info('Slave sending message same...')
      send_message(input(), cable_serial, prng)
      # logging.info('Slave finished...')

def main(args):
  if args.slave:
    slave(args.port)
  else:
    master(args.port)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--slave', action='store_true', default=False)
  parser.add_argument('--port', type=str, default=DEFAULT_PORT)
  args = parser.parse_args()
  main(args)

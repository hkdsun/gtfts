#!/bin/python

import RPi.GPIO as GPIO
import time
import socket

HOSTNAME = 'h8pc.local'
PORT = 8098
BUFF_SIZE = 1024
I_LED = 20
I_UP = 19
I_DOWN = 5

I_B0 = 4
I_B1 = 17
I_B2 = 27
I_B3 = 22
I_B4 = 6
I_B5 = 13
I_B6 = 26
I_B7 = 18

def refresh_socket(host, port):
  while True:
    try:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect((HOSTNAME, PORT))
    except socket.error as e:
      print("Could not connect to {}:{}. Retrying in 5 seconds".format(host, port))
      time.sleep(5)
      continue
    print("Connected to {}:{}".format(host, port))
    break
  return s

def idle():
  GPIO.output(I_LED, True)

def unidle():
  GPIO.output(I_LED, False)

def volume_up(socket):
  socket.sendall("V-")

def volume_up(socket):
  socket.sendall("V+")

def volume_down(socket):
  socket.sendall("V-")


def setup():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(I_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(I_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(I_LED, GPIO.OUT)

def close():
  GPIO.cleanup()

def loop():
  s = refresh_socket(HOSTNAME, PORT)
  while True:
    if GPIO.input(I_UP) == False:
      unidle()
      try:
        volume_up(s)
      except socket.error as e:
        print("Disconnected due to: {}".format(e))
        s.close()
        s = refresh_socket(HOSTNAME, PORT)
      time.sleep(0.1)
    if GPIO.input(I_DOWN) == False:
      unidle()
      try:
        volume_down(s)
      except socket.error as e:
        print("Disconnected due to: {}".format(e))
        s.close()
        s = refresh_socket(HOSTNAME, PORT)
      time.sleep(0.1)
    idle()

if __name__ == "__main__":
  try:
    setup()
    loop()
  except KeyboardInterrupt:
    close()

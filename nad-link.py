#!/usr/bin/env python

OutPin = 7
Config = {  # This configuration is for my C350

  'off':    ('once', 0xe13e01fe),
  'on':     ('once', 0xe13e01fe),
  'power':     ('once', 0xe13e01fe),

  'mute':     ('once', 0xe13e29d6),

  # Volume
  #
  '-':      ('hold', 0xe13e31ce),
  'down':     ('hold', 0xe13e31ce),
  '+':      ('hold', 0xe13e11ee),
  'up':       ('hold', 0xe13e11ee),

  'monitor':  ('once', 0xe13eb14e),
  'tape':     ('once', 0xe13e8976),
  'tuner':    ('once', 0xe13e41be),
  'aux':      ('once', 0xe13ed926),
  'video':    ('once', 0xe13e03fc),
  'cd':       ('once', 0xe13ea15e),
  'phono':    ('once', 0xe13e916e),

  'src-':     ('once', 0xe13eb847),
  'src+':     ('once', 0xe13e58a7),

  # Personal source aliases :D
  #
  'radio':    ('once', 0xe13ebb44),
  'sofa':     ('once', 0xe13ed926),
  'pi':       ('once', 0xe13e43bc),
  'mac':      ('once', 0xe13ea15e)
}


# Catch ^C (SIGINT) and handle politely
#
carryOn = True  # yayyy global
#
import signal
def sigint_handler(signal, frame):
  global carryOn
  carryOn = False
signal.signal(signal.SIGINT, sigint_handler)


import RPi.GPIO as g
import time
import sys
import os
import atexit

from monotonic import monotonic


def cleanup():
  g.cleanup(OutPin)
atexit.register(cleanup)

g.setmode(g.BOARD)
g.setup(OutPin, g.OUT, initial=True)

try:
	mode, cmd = Config[sys.argv[1]]
except (KeyError, IndexError):
	try:
		mode = str(sys.argv[1])
		if mode != 'once' and mode != 'hold':
			print("ERROR: The first argument can only take 'once' or 'hold'")		 
			print("The wrong value is:", mode)
			exit()
		
		try:
			try:
				arg_type = sys.argv[3]
				if arg_type == 'int':
					cmd = int(sys.argv[2])
				elif arg_type == 'hex' or arg_type == 'hexadecimal':
					cmd = int(sys.argv[2], 16)
				else:
					print("WARNING: the third argument was neither hex nor int, and will not be taken into consideration. \n the default type 'hex' will be used")
					cmd = int(sys.argv[2], 16)
			except IndexError:	
				cmd = int(sys.argv[2], 16)
		except ValueError:
			print("ERROR: Not a valid hex code was entered as second argument")
			print("The entered hex code is:", cmd)
			exit()

	except:
		print("Usage: give a known funcion as argument, or give two arguments, the first being: <mode>, this takes a value of either hold or once. The second argument is a hex code <hex code>")
		exit()

hold = mode.lower() == 'hold'


# The magic durations between output state flips that represent a single remote-control signal bit in NAD-land
#
def oneBitDelays(bit):
  yield 560
  yield (1690 if bit else 560)


# The magic durations between output state flips for an entire command.
#
def commandDelays(cmd):
  if not carryOn:
    exit(0)  # let us quit before we even begin!

  # Send preamble
  yield 9000
  yield 4500

  # Send the remote code one bit at a time
  print("The value is:", cmd, "And the type is:", type(cmd))
  for c in "{0:b}".format(cmd):
    for d in oneBitDelays(c=='1'):
      yield d

  # Terminate the command
  yield 560
  yield 42020

  # Send repeats until ^C in case of hold commands.
  # I love that Python generators are properly lazy and therefore this disgusting use of shared 'carryOn' state actually works.
  if hold:
    while carryOn:
      yield 9000
      yield 2250
      yield 560
      yield 98190


# Transformation of the 'between flip durations' iterator into an iterator over actual absolute moments in time.
# This an attempt to improve timing precision by stopping delay errors accumulating, calculating all delays relative to the start of the event.
# As I don't have an oscilloscope or anything like that, I cannot really tell whether it works.
# Subjectively, this script seems to successfully trigger the amp more often than the last version...
#
def flippingInstants(cmd, firstInstant):
  last = 0
  for d in commandDelays(cmd):
    if last > 0:
      yield firstInstant + (last * 0.000001)
    last += d


currentState = True

now = monotonic()
currentState = not currentState
g.output(OutPin, currentState)

for i in flippingInstants(cmd, now):
  while monotonic() < i:
    pass
  currentState = not currentState
  g.output(OutPin, currentState)

assert(currentState == True)  # We had an even number of output flips and ended up where we started (I didn't forget a yield. (Perhaps I forgot two though.))
print("The program has probably executed succesfully")

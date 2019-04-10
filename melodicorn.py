import RPi.GPIO as GPIO
import time
import pygame as pg
GPIO.setmode(GPIO.BCM)

pg.mixer.init(44100, -16, 2, 2048)

# GPIO pins to source and sink.
# Sinking through cols because that's how I soldered the diodes.
cols = [27, 22, 23]
rows = [20, 24, 25, 5, 6, 12, 13, 16]

# Tuple of (row,col) to filename.
filenames = {
# Keys (sustain)
(22, 6):  "wavs/wav-reco/1.wav",
(22, 5):  "wavs/wav-reco/2.wav",
(22, 25): "wavs/wav-reco/3.wav",
(23, 24): "wavs/wav-reco/4.wav",
(23, 25): "wavs/wav-reco/5.wav",
(23, 5):  "wavs/wav-reco/6.wav",
(23, 6):  "wavs/wav-reco/7.wav",
(23, 12): "wavs/wav-reco/8.wav",
(23, 13): "wavs/wav-reco/9.wav",
(23, 16): "wavs/wav-reco/10.wav",
(23, 20): "wavs/wav-reco/11.wav",

# Strings (impulse)
(22, 13): "wavs/wav-down/1.wav",
(22, 16): "wavs/wav-down/2.wav",
(22, 20): "wavs/wav-down/3.wav",
(27, 24): "wavs/wav-down/4.wav",
(27, 25): "wavs/wav-down/5.wav",
(27, 5): "wavs/wav-down/6.wav",
(27, 6): "wavs/wav-down/7.wav",
(27, 12): "wavs/wav-down/8.wav",
(27, 13): "wavs/wav-down/9.wav",
(27, 16): "wavs/wav-down/10.wav",
(27, 20): "wavs/wav-down/11.wav",
}

# If these are all set, restart.
# Emergency for those times when sound gets jitery.
resets = [
(22, 6),
(22, 5),
(22, 25),
(23, 24),
(23, 25),
(23, 5),
(23, 6),
(23, 12),
(23, 13),
(23, 16),
(23, 20),
]

resets_set = set(resets)

sounds = {}
for (k, path) in filenames.items():
  sounds[k] = pg.mixer.Sound(path)
  sounds[k].set_volume(0.20)

def start(k):
  if k in sounds:
    sounds[k].play()

def stop(k):
  if k in sounds:
    sounds[k].fadeout(200)

# Warning sound, then exit.
# Assume script will be restarted.
def reset():
  for x in resets:
    stop(x)
  for x in resets:
    start(x)
    time.sleep(0.05)
    stop(x)
  exit(0)

cols = [27, 22, 23]
rows = [20, 24, 25, 5, 6, 12, 13, 16]

## Global state. Shared between interrupt handler, row scanner and detector.

# Current col being iterated.
col = None

# Previous keys that were down.
prev = set()

# Keys that are currently down.
next = set()

def callback(pin):
  global next
  print(pin)
  if col:
    val = (col, pin)
    next.add(val)

# Initialize GPIOs.
for x in cols:
  #if GPIO.gpio_function(x) == GPIO.IN:
  #  GPIO.remove_event_detect(x)
  GPIO.setup(x, GPIO.OUT)

for x in rows:
  if GPIO.gpio_function(x) == GPIO.IN:
    GPIO.remove_event_detect(x)
  GPIO.setup(x, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  #GPIO.add_event_detect(x, GPIO.FALLING, callback=callback)

# Main loop to set cols, detect rows.
# HIGH is 'off'.
while True:
  next = set()
  # Clear rows
  for x in cols:
    GPIO.output(x, GPIO.HIGH)

  # Set this col 'on'.
  for x in cols:
    GPIO.output(x, GPIO.LOW)
    time.sleep(0.005)

    # State change detection.
    for r in rows:
      v = (x, r)
      if not GPIO.input(r):
        if v not in prev:
          start(v)
        next.add(v)
      else:
        if v in prev:
          stop(v)     
    GPIO.output(x, GPIO.HIGH)
  prev = next
  next = set()

  # If the right keys are pressed, exit.
  if prev.intersection(resets_set) == resets_set:
    reset()

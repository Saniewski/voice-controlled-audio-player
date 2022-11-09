import sounddevice as sd
import numpy as np

second = 1000

def callback(indata, outdata, frames, time, status):
  if status:
    print(status)
  volume_norm = np.linalg.norm(indata)*10
  print("|" * int(volume_norm))

with sd.Stream(callback=callback):
  sd.sleep(60 * second)

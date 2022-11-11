from utils import get_logger
# import sounddevice as sd
import pyaudio
import numpy as np
import pika, io, wave

logger = get_logger(__name__)

class CommandInterpreter:

  mq_host = 'localhost'
  mq_port = 5672
  mq_queue = 'commands'

  
  def __init__(self):
    self.mq_connection = pika.BlockingConnection(
      pika.ConnectionParameters(host=self.mq_host, port=self.mq_port))
    self.mq_channel = self.mq_connection.channel()
    self.mq_channel.queue_declare(queue=self.mq_queue)
  

  def run(self):
    logger.info("Command Interpreter is running and listening \
      with a built-in microphone for commands")
    
    p = pyaudio.PyAudio()

    stream = p.open(
      format=pyaudio.paInt16,
      channels=1,
      rate=16000,
      input=True,
      frames_per_buffer=1024)

    frames = []
    for i in range(0, int(16000 / 1024 * 5)):
      data = stream.read(1024)
      as_ints = array('h', data)
      max_value = max(as_ints)
      if max_value > 10:
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p,terminate()

    wf = wave.open('output.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    wf.writeframes(b''.join(frames))
    wf.close()
    # with sd.InputStream(
    #   channels=1,
    #   samplerate=16000,
    #   callback=self.callback
    # ):
    #   while True:
    #     sd.sleep(3000)

    #     self.stop = True
    #     data = np.concatenate(self.all_data)
    #     write('output.wav', 16000, data)
    #     return
  

  def teardown(self):
    self.mq_connection.close()
  

  # def callback(self, indata, outdata, frames, time):
  #   # if status:
  #     # logger.debug(status)
  #     # self.mq_channel.basic_publish(exchange='', routing_key=self.mq_queue, body=status)
  #   if not self.stop:
  #     self.all_data.append(indata)
  #   # self.mq_channel.basic_publish(exchange='', routing_key=self.mq_queue, body=body)
  

if __name__ == '__main__':
  logger.info('Starting Command Interpreter...')

  worker = CommandInterpreter()
  
  try:
    worker.run()
  except KeyboardInterrupt:
    worker.teardown()
  
  logger.info('Command Interpreter stopped.')

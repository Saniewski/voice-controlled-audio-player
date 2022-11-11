from utils import get_logger
import os, pika, pyaudio, threading, wave
# import matplotlib.pyplot as plt
# import numpy as np
from speechbrain.pretrained import EncoderDecoderASR
from thefuzz import fuzz


logger = get_logger(__name__)

class CommandInterpreter:

  mq_host = 'localhost'
  mq_port = 5672
  mq_queue = 'commands'
  audio_format = pyaudio.paInt16
  audio_sample_rate = 16000
  audio_channels = 1
  audio_chunk_size = 1024
  audio_batch_seconds = 5
  commands = [
    'play',
    'pause',
    'next',
    'previous',
    'rewind',
    'mute',
    'unmute'
  ]
  fuzz_threshold = 50

  
  def __init__(self):
    self.is_command_mode = False
    logger.debug('Initializing RabbitMQ connection...')
    self.mq_connection = pika.BlockingConnection(
      pika.ConnectionParameters(host=self.mq_host, port=self.mq_port))
    logger.debug('Setting up RabbitMQ channel...')
    self.mq_channel = self.mq_connection.channel()
    logger.debug('Declaring RabbitMQ queue...')
    self.mq_channel.queue_declare(queue=self.mq_queue)

    logger.debug('Loading ASR model...')
    self.asr_model = EncoderDecoderASR.from_hparams(
      source="speechbrain/asr-crdnn-rnnlm-librispeech",
      savedir="pretrained_models/asr-crdnn-rnnlm-librispeech")

    logger.debug('Initializing PyAudio...')
    self.audio_capture = pyaudio.PyAudio()
    logger.debug('Opening audio stream...')
    self.audio_stream = self.audio_capture.open(
        format=self.audio_format,
        channels=self.audio_channels,
        rate=self.audio_sample_rate,
        input=True,
        frames_per_buffer=self.audio_chunk_size)
    logger.debug('Finished initializing Command Interpreter.')
  

  def run(self):
    logger.info("Command Interpreter is running and listening for commands using a built-in microphone...")
    
    frames = []
    while True:
      for _ in range(0, int(self.audio_sample_rate / self.audio_chunk_size * self.audio_batch_seconds)):
        data = self.audio_stream.read(self.audio_chunk_size)
        frames.append(data)

      batch_frames = b''.join(frames)
      frames.clear()

      logger.debug('Starting interpretation subprocess...')
      interpretation_thread = threading.Thread(target=self.interpretation_subprocess, args=(batch_frames,))
      interpretation_thread.start()
  

  # TODO: convert interpretation_subprocess to a PyAudio callback
  def interpretation_subprocess(self, frames):
    ### Plotting audio frames for debugging purposes
    # audio_ints = np.frombuffer(frames, dtype=np.int16, count=len(frames)//2, offset=0)
    # audio_floats = audio_ints * .5**15
    # plt.figure(figsize=(10, 4))
    # plt.plot(audio_floats)
    # plt.show()

    logger.debug('Building wave file...')
    wf = wave.open('tmp.wav', 'wb')
    wf.setnchannels(self.audio_channels)
    wf.setsampwidth(self.audio_capture.get_sample_size(self.audio_format))
    wf.setframerate(self.audio_sample_rate)
    wf.writeframes(frames)
    wf.close()

    logger.debug('Transcribing audio...')
    transcription = self.asr_model.transcribe_file('tmp.wav').replace(' ', '').lower()
    os.remove('tmp.wav')
    logger.debug(f"Transcription: {transcription}")

    logger.debug('Finding best match...')
    command = self.match_transcription_to_command(transcription)
    logger.debug(f"Matched command: {command}")

    self.handle_command(command)
  

  def teardown(self):
    logger.debug('Teardown sequence started...')
    logger.debug('Closing RabbitMQ connection...')
    self.mq_connection.close()
    logger.debug('Stopping audio stream...')
    self.audio_stream.stop_stream()
    logger.debug('Closing audio stream...')
    self.audio_stream.close()
    logger.debug('Terminating PyAudio...')
    self.audio_capture.terminate()
    logger.debug('Finished teardown sequence.')
  
  
  def handle_command(self, command):
    if command == 'hey-player':
        logger.debug('Activating command mode...')
        self.mq_channel.basic_publish(exchange='', routing_key=self.mq_queue, body='hey-player-set-command-mode')
        self.is_command_mode = True
    elif self.is_command_mode:
      if command in self.commands:
        logger.debug(f'Command matched! Deactivating command mode and running command "{command}"...')
        self.mq_channel.basic_publish(
          exchange='',
          routing_key=self.mq_queue,
          body='hey-player-unset-command-mode')
        self.is_command_mode = False
        self.mq_channel.basic_publish(exchange='', routing_key=self.mq_queue, body=command)
    else:
      # logger.debug('Unknown command. Deactivating command mode...')
      self.mq_channel.basic_publish(exchange='', routing_key=self.mq_queue, body='hey-player-unset-command-mode')
      self.is_command_mode = False
  

  def match_transcription_to_command(self, transcription):
    if not self.is_command_mode:
      logger.debug(f'hey-player fuzz: {fuzz.ratio(transcription, "hey player")}')
      return 'hey-player' if fuzz.ratio(transcription, 'hey player') > self.fuzz_threshold else None
    
    fuzz_scores = {}
    for command in self.commands:
      fuzz_scores[command] = fuzz.ratio(transcription, command)
    
    logger.debug('Fuzz scores:')
    for k in fuzz_scores.keys():
      logger.debug(f'\t{k}: {fuzz_scores[k]}')

    predicted_command = max(fuzz_scores, key=fuzz_scores.get)
    if fuzz_scores[predicted_command] < self.fuzz_threshold:
      return None
    return predicted_command
  

if __name__ == '__main__':
  logger.info('Starting Command Interpreter...')

  try:
    worker = CommandInterpreter()
  except Exception as e:
    logger.error(f'Failed to initialize Command Interpreter: {e}')
    exit(1)

  try:
    worker.run()
  except KeyboardInterrupt:
    worker.teardown()
  except Exception as e:
    logger.error(f'Worker run failed: {e}')
    worker.teardown()
    exit(1)
  
  logger.info('Command Interpreter has stopped.')

from player_controls import PlayerControls
from utils import get_logger
import pika

logger = get_logger(__name__)

class VoiceController:

  host = 'localhost'
  port = 5672
  queue = 'commands'

  
  def __init__(self):
    self.connection = pika.BlockingConnection(
      pika.ConnectionParameters(host=self.host, port=self.port))
    self.channel = self.connection.channel()
    self.channel.queue_declare(queue=self.queue)
    self.player = PlayerControls()
  

  def run(self):
    logger.info("Voice Controller is running")
    self.player.open_player()

    self.channel.basic_consume(
      queue=self.queue,
      auto_ack=True,
      on_message_callback=self.callback
    )

    self.channel.start_consuming()
  

  def teardown(self):
    self.connection.close()
    self.player.close_player()
  

  def callback(self, ch, method, properties, body):
    logger.debug(body)
    if body == 'hey-player-set-command-mode':
      self.player.set_command_mode()
    elif body == 'hey-player-unset-command-mode':
      self.player.unset_command_mode()
    elif body == 'play':
      self.player.click_play()
    elif body == 'pause':
      self.player.click_pause()
    elif body == 'next':
      self.player.click_next()
    elif body == 'previous':
      self.player.click_previous()
    elif body == 'rewind':
      self.player.click_rewind()
    elif body == 'mute':
      self.player.click_mute()
    elif body == 'unmute':
      self.player.click_unmute()
    else:
      logger.warning(f'Unknown command: {body}')
  

if __name__ == '__main__':
  logger.info('Starting Voice Controller...')

  worker = VoiceController()
  
  try:
    worker.run()
  except KeyboardInterrupt:
    worker.teardown()
  
  logger.info('Voice Controller has stopped.')

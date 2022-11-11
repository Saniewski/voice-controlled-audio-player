from utils import get_logger
from player_controls import PlayerControls
import pika


logger = get_logger(__name__)

class VoiceController:

  mq_host = 'localhost'
  mq_port = 5672
  mq_queue = 'commands'

  
  def __init__(self):
    logger.debug('Initializing RabbitMQ connection...')
    self.mq_connection = pika.BlockingConnection(
      pika.ConnectionParameters(host=self.mq_host, port=self.mq_port))
    logger.debug('Setting up RabbitMQ channel...')
    self.mq_channel = self.mq_connection.channel()
    logger.debug('Declaring RabbitMQ queue...')
    self.mq_channel.queue_declare(queue=self.mq_queue)

    logger.debug('Initializing player...')
    self.player = PlayerControls()
    logger.debug('Finished initializing Voice Controller.')
  

  def run(self):
    logger.info("Running Voice Controller...")
    try:
      logger.debug("Opening audio player...")
      self.player.open_player()
    except Exception as e:
      logger.error(f'Failed to open player: {e}')
      return

    try:
      logger.debug("Setting up RabbitMQ basic consume...")
      self.mq_channel.basic_consume(
        queue=self.mq_queue,
        auto_ack=True,
        on_message_callback=self.callback
      )
    except Exception as e:
      logger.error(f'Failed to setup consume: {e}')
      return

    try:
      logger.debug("Voice Controller is running and listening for commands.")
      self.mq_channel.start_consuming()
    except Exception as e:
      logger.error(f'Failed to start consuming RabbitMQ messages: {e}')
      return
  

  def teardown(self):
    logger.debug('Teardown sequence started...')
    logger.debug('Stopping consuming RabbitMQ messages...')
    self.mq_channel.stop_consuming()
    logger.debug('Closing RabbitMQ channel...')
    self.mq_channel.close()
    logger.debug('Closing RabbitMQ connection...')
    self.mq_connection.close()
    logger.debug('Closing player...')
    self.player.close_player()
    logger.debug('Finished teardown sequence.')
  

  def callback(self, ch, method, properties, body):
    logger.debug(body)
    if body == b'hey-player-set-command-mode':
      self.player.set_command_mode()
    elif body == b'hey-player-unset-command-mode':
      self.player.unset_command_mode()
    elif body == b'play':
      self.player.click_play()
    elif body == b'pause':
      self.player.click_pause()
    elif body == b'next':
      self.player.click_next()
    elif body == b'previous':
      self.player.click_previous()
    elif body == b'rewind':
      self.player.click_rewind()
    elif body == b'mute':
      self.player.click_mute()
    elif body == b'unmute':
      self.player.click_unmute()
    else:
      logger.warning(f'Unknown command: {body}')
  

if __name__ == '__main__':
  logger.info('Starting Voice Controller...')

  try:
    worker = VoiceController()
  except Exception as e:
    logger.error(f'Failed to initialize Voice Controller: {e}')
    exit(1)
  
  try:
    worker.run()
  except KeyboardInterrupt:
    worker.teardown()
  except Exception as e:
    logger.error(f'Worker run failed: {e}')
    exit(1)
  
  logger.info('Voice Controller has stopped.')

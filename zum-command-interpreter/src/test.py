from main import CommandInterpreter

worker = CommandInterpreter()
  
try:
  worker.run()
except KeyboardInterrupt:
  worker.teardown()

while True:

  value = input('Enter command: ')

  if value == '1':
    worker.handle_command('hey-player-set-command-mode')
  elif value == '2':
    worker.handle_command('hey-player-unset-command-mode')
  elif value == '3':
    worker.handle_command('play')
  elif value == '4':
    worker.handle_command('pause')
  elif value == '5':
    worker.handle_command('next')
  elif value == '6':
    worker.handle_command('previous')
  elif value == '7':
    worker.handle_command('rewind')
  elif value == '8':
    worker.handle_command('mute')
  elif value == '9':
    worker.handle_command('unmute')

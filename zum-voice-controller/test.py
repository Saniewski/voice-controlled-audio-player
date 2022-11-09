from player_controls import PlayerControls
import time
import subprocess

command = 'python3 -m http.server --directory ../zum-audio-player'

http_server = subprocess.Popen(command.split(' '))

time.sleep(5)

player = PlayerControls()
player.open_player()

time.sleep(5)

player.click_play()

time.sleep(5)

player.click_mute()

time.sleep(5)

player.click_mute()

time.sleep(5)

player.click_unmute()

time.sleep(5)

player.click_unmute()

time.sleep(5)

player.click_next()

time.sleep(5)

player.click_previous()

time.sleep(10)

player.click_rewind()

time.sleep(5)

player.click_pause()

time.sleep(5)

player.click_play()

time.sleep(5)

player.click_play()

time.sleep(5)

player.click_pause()

time.sleep(5)

player.click_pause()

time.sleep(5)

http_server.kill()

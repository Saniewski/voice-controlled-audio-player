from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from xpaths import xpaths


class PlayerControls:

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def open_player(self):
        self.driver.get('http://localhost:8000')

    def click(self, xpath):
        try:
            element = self.driver.find_element('xpath', xpath)
            element.click()
            print('Clicked!')
        except Exception as e:
            print('Element not found')

    def click_next(self):
        print('Clicking next...')
        self.click(xpaths['next'])

    def click_previous(self):
        print('Clicking previous...')
        self.click(xpaths['previous'])

    def click_play(self):
        print('Clicking play...')
        self.click(xpaths['play'])
    
    def click_pause(self):
        print('Clicking pause...')
        self.click(xpaths['pause'])

    def click_rewind(self):
        print('Clicking rewind...')
        self.click(xpaths['rewind'])

    def click_mute(self):
        print('Clicking mute...')
        self.click(xpaths['mute'])
    
    def click_unmute(self):
        print('Clicking unmute...')
        self.click(xpaths['unmute'])

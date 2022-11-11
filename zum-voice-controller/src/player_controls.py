from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from xpaths import xpaths


class PlayerControls:

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.current_mode = 'normal'
        self.normal_mode_volume = None

    def open_player(self):
        self.driver.get('http://localhost:80')
    
    def close_player(self):
        self.driver.close()

    def __click(self, xpath):
        try:
            element = self.driver.find_element('xpath', xpath)
            element.click()
            print('Clicked!')
        except Exception as e:
            print('Element not found')
    
    def __execute_js(self, element, script):
        try:
            element._parent.execute_script(script, element)
            print('Executed!')
        except Exception as e:
            print('Failed to execute javascript script on element')

    def set_command_mode(self):
        print('Setting command mode...')
        element = self.driver.find_element('xpath', xpaths['audio'])
        print(element._parent)
        self.normal_mode_volume = element.get_attribute('volume')
        self.__execute_js(element, 'arguments[0].volume = arguments[0].volume * 0.2')
        self.current_mode = 'command'
    
    def unset_command_mode(self):
        print('Setting command mode...')
        element = self.driver.find_element('xpath', xpaths['audio'])
        self.__execute_js(element, f'arguments[0].volume = {self.normal_mode_volume}')
        self.current_mode = 'normal'
        self.normal_mode_volume = None

    def click_next(self):
        print('Clicking next...')
        self.__click(xpaths['next'])

    def click_previous(self):
        print('Clicking previous...')
        self.__click(xpaths['previous'])

    def click_play(self):
        print('Clicking play...')
        self.__click(xpaths['play'])
    
    def click_pause(self):
        print('Clicking pause...')
        self.__click(xpaths['pause'])

    def click_rewind(self):
        print('Clicking rewind...')
        self.__click(xpaths['rewind'])

    def click_mute(self):
        print('Clicking mute...')
        self.__click(xpaths['mute'])
    
    def click_unmute(self):
        print('Clicking unmute...')
        self.__click(xpaths['unmute'])

from utils import get_logger
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from xpaths import xpaths


logger = get_logger(__name__)

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
            logger.debug('Clicked!')
        except Exception as e:
            logger.warn('Element not found')
    
    def __execute_js(self, element, script):
        try:
            element._parent.execute_script(script, element)
            logger.debug('Executed!')
        except Exception as e:
            logger.warn('Failed to execute javascript script on element')

    def set_command_mode(self):
        logger.debug('Setting command mode...')
        element = self.driver.find_element('xpath', xpaths['audio'])
        self.normal_mode_volume = element.get_attribute('volume')
        self.__execute_js(element, 'arguments[0].volume = arguments[0].volume * 0.2')
        self.current_mode = 'command'
    
    def unset_command_mode(self):
        logger.debug('Setting normal mode...')
        element = self.driver.find_element('xpath', xpaths['audio'])
        self.__execute_js(element, f'arguments[0].volume = {self.normal_mode_volume}')
        self.current_mode = 'normal'
        self.normal_mode_volume = None

    def click_next(self):
        logger.debug('Clicking next...')
        self.__click(xpaths['next'])

    def click_previous(self):
        logger.debug('Clicking previous...')
        self.__click(xpaths['previous'])

    def click_play(self):
        logger.debug('Clicking play...')
        self.__click(xpaths['play'])
    
    def click_pause(self):
        logger.debug('Clicking pause...')
        self.__click(xpaths['pause'])

    def click_rewind(self):
        logger.debug('Clicking rewind...')
        self.__click(xpaths['rewind'])

    def click_mute(self):
        logger.debug('Clicking mute...')
        self.__click(xpaths['mute'])
    
    def click_unmute(self):
        logger.debug('Clicking unmute...')
        self.__click(xpaths['unmute'])

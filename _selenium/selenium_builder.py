from . import chrome, chromium, firefox, edge, ie, opera

from selenium.webdriver.common.by import By

class Selenium_rq:

    browserEngine = ""
    url = ""
    proxy = {}
    actions = []
    driver = None

    def __init__(self, browserEngine, url, proxy):
        self.browserEngine = browserEngine
        self.url = url
        self.proxy = proxy

        if browserEngine == "chrome":
            self.driver = chrome.init_chrome()
        elif browserEngine == "chromium":
            self.driver = chromium.init_chromium()
        elif browserEngine == "firefox":
            self.driver = firefox.init_firefox()
        elif browserEngine == "IE":
            self.driver = ie.init_ie()
        elif browserEngine == "edge":
            self.driver = edge.init_edge()
        elif browserEngine == "opera":
            self.driver = opera.init_opera()

    def selenium_actions(self, actions):
        self.driver.maximize_window()
        self.driver.get(self.url)

        #for action in actions:
        #    for act_dict in action:
        #        if action['type'] == 'find_element_by_name'
        self.driver.find_element(By.NAME, 'q').send_keys('test')

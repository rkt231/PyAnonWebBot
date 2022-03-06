from . import chrome, chromium, firefox, edge, ie, opera
from selenium.webdriver.common.by import By
import json
import time

class Selenium_rq:

    browserEngine = ""
    url = ""
    proxy = {}
    actions = []
    driver = None

    def __init__(self, browserEngine, url, proxy, headers):
        self.browserEngine = browserEngine
        self.url = url
        self.proxy = proxy

        if browserEngine == "chrome":
            self.driver = chrome.init_chrome(proxy, headers)
        elif browserEngine == "chromium":
            self.driver = chromium.init_chromium(proxy, headers)
        elif browserEngine == "firefox":
            self.driver = firefox.init_firefox(proxy, headers)
        elif browserEngine == "IE":
            self.driver = ie.init_ie(proxy)
        elif browserEngine == "edge":
            self.driver = edge.init_edge(proxy)
        elif browserEngine == "opera":
            self.driver = opera.init_opera(proxy)

    def open_url(self):
        self.driver.maximize_window()
        self.driver.get(self.url)
        time.sleep(5)

    def selenium_actions(self, actions):
        """
        Need to open action as a list form as a json
        can be a file or read directly from cli
        """
        if isinstance(actions, str):
            try:
                json_actions = json.loads(actions)
            except Exception as e:
                raise e
        else:
            try:
                json_actions = json.loads(actions.read()) 
            except Exception as e:
                raise e

        for action in json_actions:
            for sub_action in action:
                if sub_action['type'] == 'find_element_by_name':
                    action_value = sub_action['value']
                    obj_action_type = self.driver.find_element(By.NAME, \
                        action_value)
                elif sub_action['type'] == 'send_keys':
                    action_value = sub_action['value']
                    obj_action_type.send_keys(action_value)

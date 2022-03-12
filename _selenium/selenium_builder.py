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

        key_bindings = {"Keys.ENTER": '\ue007', "Keys.RETURN": '\ue006', \
            "Keys.ARROW_DOWN": '\ue015', "Keys.DOWN": '\ue015', \
            "Keys.ARROW_UP": '\ue013', "Keys.UP": '\ue013', \
            "Keys.ARROW_LEFT": '\ue012', "Keys.LEFT": '\ue012', \
            "Keys.ARROW_RIGHT": '\ue014', "Keys.RIGHT": '\ue014', \
            "Keys.BACKSPACE": '\ue003', "Keys.BACK_SPACE": '\ue003', \
            "Keys.CANCEL": '\ue001', "Keys.CLEAR": '\ue005', \
            "Keys.TAB": '\ue004', "Keys.ALT": '\ue00a', \
            "Keys.COMMAND": '\ue03d', "Keys.CONTROL": '\ue009', \
            "Keys.DELETE": '\ue017', "Keys.END": '\ue010', \
            "Keys.ESCAPE": '\ue00c', "Keys.LEFT_CONTROL": '\ue009', \
            "Keys.LEFT_ALT": '\ue00a', "Keys.LEFT_SHIFT": '\ue008', \
            "Keys.PAGE_DOWN": '\ue00f', "Keys.PAGE_UP": '\ue00e',
            "Keys.SHIFT": '\ue008', "Keys.SPACE": '\ue00d'}
        for action in json_actions:
            for sub_action in action:
                if sub_action['type'] == 'find_element_by_name':
                    action_value = sub_action['value']
                    obj_action_type = self.driver.find_element(By.NAME, \
                        action_value)
                elif sub_action['type'] == 'find_element_by_id':
                    action_value = sub_action['value']
                    obj_action_type = self.driver.find_element(By.ID, \
                        action_value)
                elif sub_action['type'] == 'send_keys':
                    action_value = sub_action['value']
                    # mapping https://www.selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html
                    if action_value in key_bindings:
                        action_value = key_bindings[action_value]
                    obj_action_type.send_keys(action_value)
                    
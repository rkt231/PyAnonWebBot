from . import chrome, chromium, firefox, edge, ie, opera
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
#import re

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
        Actions as a list of lists of dicts, as a json form
        Can be a file or read directly from cli
        Look at test_ddg.json for an example
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
        # mapping https://www.selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html            
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
            "Keys.SHIFT": '\ue008', "Keys.SPACE": '\ue00d', \
            "Keys.NULL": '\ue000', "Keys.HOME": '\ue011'}
        #key_pattern = r'Keys\.[A-Z0-9]+'
        for action in json_actions:
            for sub_action in action:
                if sub_action['type'] == "refresh":
                    self.driver.refresh()
                elif sub_action['type'] == "close":
                    self.driver.refresh()
                elif sub_action['type'] == "wait":
                    wait_time = float(sub_action['value'])
                    time.sleep(wait_time)
                elif sub_action['type'] == "ExplicitWait":
                    timeout = float(sub_action["timeout"])
                    element = sub_action["element"]
                    #if hasattr(self.driver, element["type"]) and callable(\
                    #    getattr(self.driver, element["type"])):
                    #    WebDriverWait(self.driver, timeout).until(
                    #        EC.presence_of_element_located(\
                    #            getattr(self.driver, element["type"])(\
                    #                element["value"]))
                    #        )
                    WebDriverWait(self.driver, timeout).until(
                        EC.presence_of_element_located((element["type"], 
                            element["value"]))
                        )
                else:
                    action_value = sub_action['value']
                    if sub_action['type'] == 'find_element_by_name':
                        obj_action_type = self.driver.find_element(By.NAME, \
                            action_value)
                    elif sub_action['type'] == 'find_element_by_id':
                        obj_action_type = self.driver.find_element(By.ID, \
                            action_value)
                    elif sub_action['type'] == 'find_element_by_link_text':
                        obj_action_type = self.driver.find_element(By.LINK_TEXT, \
                            action_value)
                    elif sub_action['type'] == 'find_element_by_partial_link_text':
                        obj_action_type = self.driver.find_element(
                            By.PARTIAL_LINK_TEXT, action_value)
                    elif sub_action['type'] == 'find_element_by_css_selector':
                        obj_action_type = self.driver.find_element(
                            By.CSS_SELECTOR, action_value)
                    elif sub_action['type'] == 'find_element_by_xpath':
                        obj_action_type = self.driver.find_element(
                            By.XPATH, action_value)
                    elif sub_action['type'] == 'send_keys':
                        for K_key, K_value in key_bindings.items():
                            if K_key in action_value:
                                action_value = action_value.replace(K_key, K_value)
                        #if action_value in key_bindings:
                        #    action_value = key_bindings[action_value]
                        obj_action_type.send_keys(action_value)
                    elif sub_action['type'] == 'click':
                        obj_action_type.click()
                    elif sub_action['type'] == 'submit':
                        obj_action_type.submit()
                
import json
import time
import logging
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import re
from . import chrome, chromium, firefox, edge, ie, opera

class Selenium_rq:
    """
    Selenium generic request builder
    """
    browser_engine = ""
    url = ""
    proxy = {}
    actions = []
    driver = None

    def __init__(self, browser_engine, url, proxy, headers):
        self.browser_engine = browser_engine
        self.url = url
        self.proxy = proxy

        if browser_engine == "chrome":
            self.driver = chrome.init_chrome(proxy, headers)
        elif browser_engine == "chromium":
            self.driver = chromium.init_chromium(proxy, headers)
        elif browser_engine == "firefox":
            self.driver = firefox.init_firefox(proxy, headers)
        elif browser_engine == "IE":
            self.driver = ie.init_ie(proxy, headers)
        elif browser_engine == "edge":
            self.driver = edge.init_edge(proxy, headers)
        elif browser_engine == "opera":
            self.driver = opera.init_opera(proxy, headers)

    def open_url(self):
        """
        Open URL with browser
        """
        self.driver.maximize_window()
        self.driver.get(self.url)
        time.sleep(5)

    def selenium_actions(self, actions):
        """
        Actions as a list of lists of dicts, as a json form.
        Multiple list allow multiple scenarios.
        Can be a file or read directly from cli.
        Look at test_ddg.json for an example
        """
        if isinstance(actions, str):
            try:
                json_actions = json.loads(actions)
            except Exception as err:
                raise err
        else:
            try:
                json_actions = json.loads(actions.read())
            except Exception as err:
                raise err
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
                if 'type' in sub_action:
                    logging.info(sub_action['type'])
                    if sub_action['type'] == "refresh":
                        self.driver.refresh()
                    elif sub_action['type'] == "close":
                        self.driver.quit()
                    elif sub_action['type'] == "wait":
                        wait_time = float(sub_action['value'])
                        time.sleep(wait_time)
                    elif sub_action['type'] == "ExplicitWait":
                        if 'timeout' in sub_action:
                            timeout = float(sub_action["timeout"])
                        else:
                            logging.error("Timeout is required for ExplicitWait !")
                        if 'element' in sub_action:
                            element = sub_action["element"]
                            logging.info("type: %s " % element["type"])
                            logging.info("value: %s " % element["value"])
                            obj_action_type = WebDriverWait(self.driver, timeout).until( \
                                EC.presence_of_element_located((element["type"], \
                                    element["value"])))
                        else:
                            logging.error("\"element:\" is required for ExplicitWait \
                                  (see test_ddg.json example)")
                    else:
                        if 'value' in sub_action:
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
                                for keyboard_key, keyboard_value in key_bindings.items():
                                    if keyboard_key in action_value:
                                        action_value = action_value.replace(
                                            keyboard_key, keyboard_value)
                                obj_action_type.send_keys(action_value)
                        elif sub_action['type'] == 'click':
                            obj_action_type.click()
                        elif sub_action['type'] == 'submit':
                            obj_action_type.submit()
                        else:
                            logging.warning("Action not known/understood...")
                else:
                    logging.error("\"type:\" is required !")

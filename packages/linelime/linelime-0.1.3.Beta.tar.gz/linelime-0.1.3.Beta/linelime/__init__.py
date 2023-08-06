
import requests
import json
import time

__version__ = "0.1.0 Beta"

class TimelineConfig:
    URL = "https://timeline.line.me/api/"
    SESSION_ID = ""
    HOME_ID = ""
    HEADERS = {
        "Accept" : "application/json",
        "X-Timeline-WebVersion" : "1.11.9",
        "X-Line-AcceptLanguage" : "en",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
        "Origin" : "https://timeline.line.me",
        "Referer": "https://timeline.line.me/"
    }

    def set_session(self, session):
        self.SESSION_ID = session

    def set_home_id(self, home_id):
        self.HOME_ID = home_id

    def set_header(self, key, value):
        self.HEADERS[key] = value

    def get_config(self):
        self.set_header("Cookie", "lwtl=" + self.SESSION_ID)
        config = {
            "URL" : self.URL,
            "SESSION_ID" : self.SESSION_ID,
            "HOME_ID" : self.HOME_ID,
            "HEADERS" : self.HEADERS
        }
        return config

class TimelineReader:
    FEED = {}

    def __init__(self, config):
        self.config = config.get_config
    
    def request_feed(self):
        results = requests.get(
            self.config["URL"] + 
            "/post/list.json?homeId=" + self.config["HOME_ID"] + 
            "&requestTime=" + str(time.time() * 1000), headers=self.config["HEADERS"])
        self.FEED = results.json()
    
    def get_account_name():
        return self.FEED["homeInfo"]["userInfo"]["nickname"]
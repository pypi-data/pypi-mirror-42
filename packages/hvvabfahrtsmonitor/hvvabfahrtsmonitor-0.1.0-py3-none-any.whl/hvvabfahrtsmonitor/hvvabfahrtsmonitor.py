import json
from pprint import pprint
import requests
from datetime import datetime
from jsonschema import validate
import warlock
import re
import math

class HvvAbfahrtsmonitor(object):
    def __init__(self, file, schema_file):
        self.file = file
        self.last_update = None
        self.schema_file = schema_file
        self.last_request = None
        self.times = None
        self.parsed_objects = {}
        self._init_schema()
        self._load_url_data()
        self._init_regex()
    def _init_regex(self):
        self.regex = re.compile("([-+])(\d+)")

    def _init_schema(self):
        self.schema=""
        with open(self.file) as f:
            self.schema=json.load(f)
        self.model = warlock.model_factory(self.schema)

    def _load_url_data(self):
        data=None
        with open(self.file) as f:
            data=json.load(f)["data"]
        self.urls = data

    def _request(self, url):
        headers = {"Accept":"application/json", "Content-Type":"application/vnd.api+json"}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.text
        else:
            return None
    def _parse_response(self, response):
        parsed = json.loads(response)
        obj = self.model(parsed)
        return obj

    def _get_departure_time(self, departure):
        time=datetime.strptime(departure["time"], '%H:%M')
        now=datetime.now()
        hasDelay=bool(departure["hasDelay"])
        delay = 0
        if hasDelay:
            delay = self.regex.search(departure["delay"])
            if delay:
                sign = 1
                if delay.group(1) == '-':
                    sign = -1
                delay = int(delay.group(2)) * sign
            else:
                delay = 0
        diff = time - now
        diff_minutes = math.floor(diff.seconds/60) + int(delay)
        return diff_minutes

    def _get_times_list(self, obj):
        departures_list = obj.data["attributes"]["departures"]
        departure_times=[]
        for departure in departures_list:
            departure_time = self._get_departure_time(departure)
            if departure_time is not None:
                departure_times.append(departure_time)
        return departure_times

    def _minute_since_last_request(self):
        if self.last_request:
            now = datetime.now()
            diff = (now - self.last_request)
            diff_minutes = math.floor(diff.seconds/60)
            if diff_minutes > 0:
                return True
        else:
            return True
        return False

    def _mark_request_time(self):
        self.last_request = datetime.now()

    def _update_parsed_objects(self):
        if self._minute_since_last_request() == False:
            return
        self.parsed_objects = {}
        for url in self.urls:
            pprint(url)
            response = self._request(url["url"])
            times_obj = None
            if response is not None:
                obj=self._parse_response(response)
                pprint(obj)
                self.parsed_objects[url["name"]] = obj
        self._mark_request_time()

    def get_times(self):
        self._update_parsed_objects()
        times_dict = {}
        for name, obj in self.parsed_objects.items():
            times_dict[name] = self._get_times_list(obj)
        return times_dict

    def print_objects(self):
        for obj in self.parsed_objects.values():
            pprint(obj)

from .utils import *
import os
import threading
import re
from enum import Enum
from events import Events
from .usbdevicedetector import *
import requests
import json

logger = create_logger()


class WebDriverAgentDeviceState(Enum):
    Initializing = 1
    DeviceReady = 2
    Ready = 3
    Closed = 4

    def __new__(cls, value):
        member = object.__new__(cls)
        member._value_ = value
        return member

    def __int__(self):
        return self.value


class WebDriverAgentDevice:
    def __init__(self, identifier, process):
        self.observers = {}
        self.session_id = ''
        self.server_url = ''
        self.state = WebDriverAgentDeviceState.Initializing
        self.identifier = identifier
        self.process = process
        self.thread = threading.Thread(target=WebDriverAgentDevice.run, args=[self])
        self.thread.start()

    def close(self):
        self.process.terminate()

    def run(self):
        returncode = self.process.poll()
        while returncode is None:
            line = self.process.stdout.readline()
            returncode = self.process.poll()
            line = line.strip()
            # try parse server url
            pattern = '.*ServerURLHere->(.*)<-ServerURLHere'
            result = re.match(pattern, str(line, 'utf-8'))
            if result:
                self.server_url = result.group(1)
                self.__set_state__(WebDriverAgentDeviceState.DeviceReady)
        self.__set_state__(WebDriverAgentDeviceState.Closed)

    def register_state_observer(self, cb):
        token = hash(cb)
        self.observers[token] = cb
        return token

    def unregister_state_observer(self, token):
        self.observers[token] = None

    def __dispatch_state_change_event__(self, newState, oldState):
        for key in self.observers:
            cb = self.observers[key]
            if cb:
                cb(self, newState, oldState)

    def __set_state__(self, state):
        if state is self.state:
            return
        self.__dispatch_state_change_event__(state, self.state)
        self.state = state
        if state is WebDriverAgentDeviceState.DeviceReady:
            self.sync_status()

    def __communicate_with_wda__(self, rel_url, headers=None, params=None, is_post=False, is_delete=False, return_full_response=False):
        if int(self.state) < int(WebDriverAgentDeviceState.DeviceReady):
            return None
        if is_delete:
            response = requests.delete('{0}{1}'.format(self.server_url, rel_url), data=json.dumps(params))
        elif is_post:
            response = requests.post('{0}{1}'.format(self.server_url, rel_url), data=json.dumps(params))
        else:
            response = requests.get('{0}{1}'.format(self.server_url, rel_url))
        if return_full_response:
            return response.json()
        if response.status_code is 200:
            return response.json()["value"]

    # commands wrapper for wda
    def sync_status(self):
        response = self.__communicate_with_wda__('/status', return_full_response=True)
        self.session_id = response['sessionId']
        logger.info('status sync ok: {0}'.format(self.session_id))
        self.__set_state__(WebDriverAgentDeviceState.Ready)

    def fetch_source_tree(self):
        return self.__communicate_with_wda__('/source?format=json')

    def launch_app(self, bundle_id):
        params = {
            'desiredCapabilities': {
                'bundleId': bundle_id
            }
        }
        response = self.__communicate_with_wda__('/session', is_post=True, params=params)
        self.session_id = response['sessionId']
        return response

    def quit_current_app(self):
        self.__communicate_with_wda__('/session/{0}'.format(self.session_id), is_delete=True)
        self.sync_status()

    def tap_home_button(self):
        response = self.__communicate_with_wda__('/wda/homescreen', is_post=True)
        print(response)

    def screenshot(self):
        base64_img = self.__communicate_with_wda__('/screenshot')
        return base64_img

    def deactive_app(self, time_in_secs):
        params = {
            'duration': time_in_secs
        }
        self.__communicate_with_wda__('/session/{0}/wda/deactivateApp'.format(self.session_id), is_post=True, params=params)

    def query_link_text(self, label):
        return self.query_element('link text', 'label={0}'.format(label))

    def query_element(self, using, value):
        if not self.session_id:
            return None
        params = {
            'using': using,
            'value': value
        }
        element_infos = self.__communicate_with_wda__('/session/{0}/elements'.format(self.session_id), is_post=True, params=params)
        element_ids = []
        for element_info in element_infos:
            element_ids.append(element_info['ELEMENT'])
        return element_ids

    def query_element_attr(self, eleid, path):
        value = self.__communicate_with_wda__('/session/{0}/element/{1}/{2}'.format(self.session_id, eleid, path))
        return value

    def tap_element(self, eleid):
        if not self.session_id:
            return False
        self.__communicate_with_wda__('/session/{0}/element/{1}/click'.format(self.session_id, eleid), is_post=True)
        return True

    def input_element(self, eleid, text):
        params = {
            'value': list(text)
        }
        self.__communicate_with_wda__('/session/{0}/element/{1}/value'.format(self.session_id, eleid), is_post=True, params=params)

    def do_drag(self, from_x, from_y, to_x, to_y, duration):
        params = {
            'duration': duration,
            'fromX': from_x,
            'fromY': from_y,
            'toX': to_x,
            'toY': to_y
        }
        self.__communicate_with_wda__('/session/{0}/wda/element/0/dragfromtoforduration'.format(self.session_id), is_post=True, params=params)

    def do_tap(self, x, y):
        params = {
            'x': x,
            'y': y
        }
        self.__communicate_with_wda__('/session/{0}/wda/tap/0'.format(self.session_id),
                                      is_post=True, params=params)

    def get_alert(self):
        alert_text = self.__communicate_with_wda__('/session/{0}/alert/text'.format(self.session_id))
        return alert_text

    def accept_alert(self):
        self.__communicate_with_wda__('/session/{0}/alert/accept'.format(self.session_id), is_post=True)

    def dismiss_alert(self):
        self.__communicate_with_wda__('/session/{0}/alert/dismiss'.format(self.session_id), is_post=True)

    def match_touchid(self, is_match):
        params = {
            "match": is_match
        }
        self.__communicate_with_wda__('/session/{0}/wda/touch_id'.format(self.session_id), is_post=True, params=params)


WEB_DRIVER_AGENT_PATH = "/Users/yangwang/Documents/Projects/OnGit/WebDriverAgent"


class WebDriverAgent:
    def __init__(self, web_driver_agent_proj_path=WEB_DRIVER_AGENT_PATH):
        self.device_events = Events()
        self.usb_device_detector = USBDeviceDetector()
        self.web_driver_agent_proj_path = web_driver_agent_proj_path
        self.device_list = {}
        self.logger = create_logger()

    def any_device(self):
        return list(self.device_list.values())[0]

    def usb_device_changed(self, ids, removed_ids, added_ids):
        for removed_id in removed_ids:
            if removed_id in self.device_list:
                self.device_list[removed_id].close()

        for added_id in added_ids:
            self.run_test_on_device(added_id)

    def enable_device_auto_start(self):
        self.usb_device_detector.events.on_change += lambda ids, removed_ids, added_ids: self.usb_device_changed(ids,
                                                                                                                 removed_ids,
                                                                                                                 added_ids)
        self.usb_device_detector.start()

    def run_test_on_device(self, deviceId):
        command = '''
        xcodebuild -project {0}/WebDriverAgent.xcodeproj \
           -scheme WebDriverAgentRunner \
           -destination 'platform=iOS,id={1}' \
           test
        '''
        command = command.format(self.web_driver_agent_proj_path, deviceId)
        args = shlex.split(command)
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        real_device = WebDriverAgentDevice(deviceId, p)
        real_device.register_state_observer(
            lambda device, new_state, old_state: self.device_state_change(device, new_state, old_state))
        logger.info("{0} is initializing...".format(real_device.identifier))
        self.device_list[real_device.identifier] = real_device

    def device_state_change(self, device, newState, oldState):
        self.device_events.on_change(device, newState, oldState)
        if newState == WebDriverAgentDeviceState.DeviceReady:
            logger.info("{0} is ready, server url: {1}".format(device.identifier, device.server_url))
        if newState == WebDriverAgentDeviceState.Closed:
            self.device_list.pop(device.identifier)
            logger.info("{0} is closed, server url: {1}".format(device.identifier, device.server_url))

    def run_test_on_sim(self):
        command = '''
        xcodebuild -project {0}/WebDriverAgent.xcodeproj \
           -scheme WebDriverAgentRunner \
           -destination 'platform=iOS Simulator,name=iPhone X,OS=12.1' \
           test
        '''
        command = command.format(self.web_driver_agent_proj_path)
        args = shlex.split(command)
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sim_device = WebDriverAgentDevice("sim", p)
        sim_device.register_state_observer(
            lambda device, new_state, old_state: self.device_state_change(device, new_state, old_state))
        logger.info("{0} is initializing...".format(sim_device.identifier))
        self.device_list[sim_device.identifier] = sim_device

    def clear(self):
        for key in self.device_list:
            device = self.device_list[key]
            device.close()
        self.device_list.clear()

    def print_desc(self):
        print("{0} Agents Active.".format(len(self.device_list)))
        for key in self.device_list:
            print("{0}".format(key))

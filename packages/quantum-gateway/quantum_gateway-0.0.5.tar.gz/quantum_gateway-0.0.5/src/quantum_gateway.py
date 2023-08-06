import hashlib
import json
from http.cookies import SimpleCookie

import requests
import urllib3

TIMEOUT = 5


class QuantumGatewayScanner:
    def __init__(self, host, password, use_https=True):

        self.verify = False
        
        if use_https:
            self.scheme = 'https'
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        else:
            self.scheme = 'http'

        self.host = self.scheme + '://' + host
        self.password = password
        self.connected_devices = {}

        self.session = requests.Session()

        self.success_init = self._check_auth()

    def scan_devices(self):
        self.connected_devices = {}
        if self._check_auth():
            self._get_connected_devices()
        return self.connected_devices.keys()

    def get_device_name(self, device):
        return self.connected_devices.get(device)

    def _get_connected_devices(self):
        devices_raw = self.session.get(self.host + '/api/devices', timeout=TIMEOUT, verify=self.verify)
        devices = json.loads(devices_raw.text)
        self.connected_devices = {device['mac']: device['name'] for device in devices if device['status']}

    def _check_auth(self):
        res = self.session.get(self.host + '/api/devices', timeout=TIMEOUT, verify=self.verify)
        if res.status_code == 200:
            return True

        getLogin = self.session.get(self.host + '/api/login', timeout=TIMEOUT, verify=self.verify)
        salt = getLogin.json()['passwordSalt']

        encodedPassword = hashlib.sha512()
        encodedPassword.update((self.password + salt).encode('ascii'))

        payload = json.dumps({"password": encodedPassword.hexdigest()})

        postLogin = self.session.post(self.host + '/api/login', data=payload, timeout=TIMEOUT, verify=self.verify)
        token = SimpleCookie(postLogin.headers.get('set-cookie'))['XSRF-TOKEN'].value

        self.session.headers.update({'X-XSRF-TOKEN': token})

        res = self.session.get(self.host + '/api/devices', timeout=TIMEOUT, verify=self.verify)
        if res.status_code == 200:
            return True
        return False

    def _log_out(self):
        self.session.get(self.host + '/api/logout', timeout=TIMEOUT, verify=self.verify)
        self.session.close()

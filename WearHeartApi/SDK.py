import re

import crypto
import sys

sys.modules['Crypto'] = crypto

from base64 import b64decode
from base64 import b64encode
from Crypto.Cipher import AES
import base64
import json
import requests
import pendulum

# Padding for the input string --not
# related to encryption itself.
BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


class AESCipher:
    """
    Taken from https://blog.csdn.net/liujingqiu/article/details/79641670
    Tested under Python 3.x and PyCrypto 2.6.1.
    """

    def __init__(self, key):
        # 加密需要的key值
        self.key = key

    def encrypt(self, raw):
        raw = pad(raw)
        # 通过key值，使用ECB模式进行加密
        cipher = AES.new(self.key, AES.MODE_ECB)
        # 返回得到加密后的字符串进行解码然后进行64位的编码
        return base64.b64encode(cipher.encrypt(raw)).decode('utf8')

    def decrypt(self, enc):
        # 首先对已经加密的字符串进行解码
        enc = b64decode(enc)
        # 通过key值，使用ECB模式进行解密
        cipher = AES.new(self.key, AES.MODE_ECB)
        return unpad(cipher.decrypt(enc)).decode('utf8')


class WearHeart:

    def __init__(self, uid=None):
        """
        @todo update docs
        """
        self.encryption_key = "wo.szzhkjyxgs.20"
        self.last_request_dt = None
        self.uid = uid
        self.profile = {}

        # @todo figure out this constant
        self.c = "ctl000016"

        # censored the uid
        self.is_censored = True

        self.last_response = None

        self._reset_last_request_dt()

    def set_is_censored(self, bool=True):
        """
        :param bool:
        :return:
        """
        self.is_censored = bool

    def set_uid(self, uid):
        """
        Backdoor to the data, once we knew the uid then all her data can be
        retrieved without authentication
        @todo update docs
        """
        self.uid = uid

    def login(self, email, password):
        """
        The login is to retrieve the preference and uid.
        uid is kind of unresetable secret token. Never share
        your uid to someone else.
        @todo update docs
        """
        payload = {
            "c": "ctl000001",
            "m": "gL",
            "t": pendulum.now().int_timestamp,
            "data": {
                "c_mobile": "",
                "c_password": password,
                "c_eq_id": "",
                "c_eq_type": "lge  LG-H818",
                "c_eq_os": "5.1.1",
                "c_mail": email,
                "c_imei": "",
                "c_app_version": "1.0.51",
                "c_offer": "Android"
            }
        }
        result = self.send_request(payload)
        if result['result'] == '1':
            self.profile = result['data']
            self.set_uid(result['data']['c_uid'])
        else:
            raise Exception("Invalid email or password")

    def _reset_last_request_dt(self):
        """
        @todo update docs
        """
        self.last_request_dt = pendulum.now().to_rfc1036_string()

    def send_request(self, payload):
        """
        @todo update docs
        """
        payload = AESCipher(self.encryption_key).encrypt(json.dumps(payload))
        # put into body
        payload = json.dumps({'body': payload})
        url = "http://www.wearheart.cn:8089/zh"
        headers = {
            'If-Modified-Since': self.last_request_dt,
            'Content-Type': "application/json; charset=utf-8",
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 5.1.1; LG-H818 Build/LYZ28N)",
            'Host': "www.wearheart.cn:8089",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", url, data=payload, headers=headers).json()
        self.last_response = response
        # Update last request datetime
        self._reset_last_request_dt()
        if 'result' in response:
            decrypted = AESCipher(self.encryption_key).decrypt(response['result'])
            if self.is_censored:
                decrypted = re.sub(r'"c_uid":\s*?"(\d+)"', '"c_uid":"-"', decrypted)
            return json.loads(decrypted)
        return None

    def get_health_data_by_page(self, date=None, page=1, pagesize=10):
        """
        @todo update docs
        """
        if date is None:
            date = pendulum.now().to_date_string()
        payload = {
            "c": self.c,
            "m": "getHealthDataByPage",
            "data": {
                "c_uid": self.uid,
                "c_diastolic": "1",
                "c_systolic": "1",
                "c_date": date,
                "page": page,
                "pagesize": pagesize
            }
        }
        return self.send_request(payload)

    def get_ecg_data(self, datetime):
        """
        @todo update docs
        datetime: datetime from summary data in get_health_data_by_page
        """
        payload = {
            "c": self.c,
            "m": "getECGData",
            "data": {
                "c_uid": self.uid,
                "c_date": datetime
            }
        }
        return self.send_request(payload)

    def get_day_heart_data(self, date=None):
        """
        @todo update docs
        """
        if date is None:
            date = pendulum.now().to_date_string()
        payload = {
            "c": "ctl000016",
            "m": "getDayHeartData",
            "data": {
                "c_uid": self.uid,
                "c_date": date
            }
        }
        return self.send_request(payload)

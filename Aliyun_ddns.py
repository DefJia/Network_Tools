import uuid
import hmac
import hashlib
import base64
import urllib
import datetime
import json
import requests
from configparser import ConfigParser


cfg = ConfigParser()
cfg.read('.config.ini')
API_ID = cfg.get('DDNS', 'API_ID')
API_KEY = cfg.get('DDNS', 'API_KEY')
domain = cfg.get('DDNS', 'Domain')
record_id = cfg.get('DDNS', 'Record_ID')
record_name = cfg.get('DDNS', 'Record_Name')
record_type = cfg.get('DDNS', 'Record_Type')
ip = cfg.get('DDNS', 'IP')
REQUEST_URL = 'https://alidns.aliyuncs.com/?'
COMMON_PARAMS = {'Format': 'json', 'Action': 'DescribeDomainRecords', 'Version': '2015-01-09', 'AccessKeyId': API_ID, 'SignatureMethod': 'HMAC-SHA1', 'Timestamp': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'), 'SignatureVersion': '1.0', 'SignatureNonce' : str(uuid.uuid1())}


class DDNS:
    def __init__(self):
        pass

    @staticmethod
    def percent_encode(encode_str):
        encode_str = str(encode_str)
        res = urllib.parse.quote(encode_str)
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return res
 
    def sign(self, parameters):
        sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
        canonicalizedQueryString = ''
        for (k, v) in sortedParameters:
            canonicalizedQueryString += '&' + self.percent_encode(k) + '=' + self.percent_encode(v)
        stringToSign = 'GET&%2F&' + self.percent_encode(canonicalizedQueryString[1:])  # 使用get请求方法
        bs = API_KEY + '&'
        bs = bytes(bs, encoding='utf8')
        stringToSign = bytes(stringToSign, encoding='utf8')
        h = hmac.new(bs, stringToSign, hashlib.sha1)
        # 进行编码
        signature = base64.b64encode(h.digest()).strip()
        return signature

    def query(self):
        COMMON_PARAMS['Action'] = 'DescribeDomainRecords'
        COMMON_PARAMS['DomainName'] = domain
        COMMON_PARAMS['Signature'] = self.sign(COMMON_PARAMS)
        sortedParameters = sorted(COMMON_PARAMS.items(), key=lambda D: D[0])
        url = REQUEST_URL + urllib.parse.urlencode(sortedParameters)
        data = requests.get(url)
        data = json.loads(data.text)
        print(data['DomainRecords'])

    def update(self):
        COMMON_PARAMS['Action'] = 'UpdateDomainRecord'
        COMMON_PARAMS['RecordId'] = record_id
        COMMON_PARAMS['RR'] = record_name
        COMMON_PARAMS['Type'] = record_type
        COMMON_PARAMS['Value'] = ip
        COMMON_PARAMS['Signature'] = self.sign(COMMON_PARAMS)
        sortedParameters = sorted(COMMON_PARAMS.items(), key=lambda D: D[0])
        url = REQUEST_URL + urllib.parse.urlencode(sortedParameters)
        try:
            data = requests.get(url)
            data = json.loads(data.text)
            # print(data)
            if 'RecordId' in data:
                print('Update successfully!')
        except Exception as e:
            print('Error,',e)


if __name__ == '__main__':
    a = DDNS()
    a.update()

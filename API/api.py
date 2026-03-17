import json
from requests import request

class API:

    @classmethod
    def do_api_test(self,data):
        method = data['method']
        if str(method).lower() == 'post':
            method = 'POST'
        elif str(method).lower() == 'get':
            method = 'GET'
        else:
            raise Exception('暂不支持POST/GET之外的请求')
        if data:
            url = data['url']
        if data == '' or data == None:
            raise "URL不能为空！"
        body = data["jsonOrparams"]
        if str(body).lower() == 'json':
            return request(method=method, json=data['data'], headers=data['header'], url=url)
        elif str(body).lower() == 'params':
            return request(method=method, params=data['data'], headers=data['header'], url=url)





# coding:utf-8
# 获取zabbix上所有主机的IP和主机名
import requests
import json
import csv
import time


class ZabbixTools:

    def __init__(self):
        self.url = "http://cube.weiche.cn/zabbix/api_jsonrpc.php"
        self.header = {"Content-Type": "application/json"}
        self.username = "Admin"
        self.password = "zabbix"

    def get_token(self):
        # data = {
        #     "jsonrpc": "2.0",
        #     "method": "user.login",
        #     "params": {
        #         "user": self.username,
        #         "password": self.password
        #     },
        #     "id": 0
        # }
        # r = requests.get(self.url, headers=self.header, data=json.dumps(data))
        # auth = json.loads(r.text)
        print(self.url, self.header, self.username, self.password)
        # return auth["result"]

    # def getHosts(token):
    #     data = {
    #         "jsonrpc": "2.0",
    #         "method": "host.get",
    #         "params": {
    #             "output": [
    #                 "hostid",
    #                 "host"
    #             ],
    #             "selectInterfaces": [
    #                 "interfaceid",
    #                 "ip"
    #             ]
    #         },
    #         "id": 2,
    #         "auth": token,
    #
    #     }
    #
    #     request = requests.post(zaurl, headers=header, data=json.dumps(data))
    #     dict = json.loads(request.content)
    #     return dict['result']



if __name__ == "__main__":
    a = ZabbixTools()
    print(a.get_token())
    # hostlist = getHosts(token)
    # datafile = "zabbix.txt"
    # fdata = open(datafile,'w')
    # for i in hostlist:
    #     hostid = i['hostid']
    #     hostip = i['host']
    #     fdata.write(hostip + ' ' + hostid + '\n')
    # fdata.close()

# coding:utf-8
# 获取zabbix上所有主机的IP和主机名
import requests
import json
import csv
import time


class ZabbixTools:

    def __init__(self):
        self.url = "http://zabbix-server-IP/zabbix/api_jsonrpc.php"
        self.header = {"Content-Type": "application/json"}
        self.username = "user"
        self.password = "password"

    def get_token(self):
        data = {
                "jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                    "user": self.username,
                    "password": self.password
                },
                "id": 1,
            }
        r = requests.get(self.url, headers=self.header, data=json.dumps(data))
        auth = json.loads(r.text)['result']
        return auth

    def get_Hosts(self, auth):
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": [
                    "hostid",
                    "host"
                ],
                "selectInterfaces": [
                    "interfaceid",
                    "ip"
                ]
            },
            "id": 2,
            "auth": auth,

        }

        request = requests.post(self.url, headers=self.header, data=json.dumps(data))
        dict = json.loads(request.content)['result']
        return dict



if __name__ == "__main__":
    a = ZabbixTools()
    hostlist = a.get_Hosts(a.get_token())
    datafile = "zabbix.txt"
    fdata = open(datafile,'w')
    for i in hostlist:
        hostid = i['hostid']
        host = i['host']
        hostip = i['interfaces'][0]['ip']
        fdata.write(hostid + ' ' + host + ' ' + hostip + '\n')
    fdata.close()

#! /usr/bin/env python2.7

import os
import sys
import json
import bareos.bsock

host = "bareos-director.local"
user = "zabbix"
password=bareos.bsock.Password("ChangeMe")

console = bareos.bsock.DirectorConsoleJson(address=host, port=9101, name=user, password=password)

# logdir = sys.argv[1]

data = []
temp = {}

jobs_list = console.call(".jobs")

for job in jobs_list['jobs']:
    temp[job['name']] = { 'enabled': str(job['enabled'])}
    job_details = console.call(".defaults job={}".format(job['name']))
    temp[job['name']]['type'] = job_details['defaults']['type']

for name in temp.keys():
    data.append(
    {'{#NAME}'      : name,
     '{#ENABLED}'   : temp[name]['enabled'],
     '{#TYPE}'      : temp[name]['type']
    }
    )


print(json.dumps({'data': data}, indent=4, separators=(',',':')))

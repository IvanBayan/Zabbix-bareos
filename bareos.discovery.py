#! /usr/bin/env python3

import os
import sys
import json
import bareos.bsock
import yaml

configfile = '/etc/zabbix/zabbix_bareos.yml'

with open(configfile, 'r') as ymlfile:
    config = yaml.load(ymlfile, yaml.SafeLoader)

user = config['user']
password = bareos.bsock.Password(config['password'])
host = config.get('host', "localhost")
port = config.get('port', 9101)

console = bareos.bsock.DirectorConsoleJson(address=host, port=port, name=user, password=password)

# logdir = sys.argv[1]

data = []
temp = {}

jobs_list = console.call(".jobs")

for job in jobs_list['jobs']:
    temp[job['name']] = { 'enabled': str(job['enabled'])}
    job_details = console.call('.defaults job="{}"'.format(job['name']))
    temp[job['name']]['type'] = job_details['defaults']['type']

for name in temp.keys():
    data.append(
    {'{#NAME}'      : name,
     '{#ENABLED}'   : temp[name]['enabled'],
     '{#TYPE}'      : temp[name]['type']
    }
    )


print(json.dumps({'data': data}, indent=4, separators=(',',':')))

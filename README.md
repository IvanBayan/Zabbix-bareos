# Template and scripts for monitoring bareos via API
That solution uses API to gather metrics from bareos, all you need to configure on bareos-dir side is a profile and user for monitoring (check examples *bareos-dir.d/console/zabbix.conf* and *bareos-dir.d/profile/monitoring.conf*)
## Features
* Gather data via API
* LLD discovery for active jobs
## Metrics & triggers
* Last job's status & size, job estimate size
* Bareos-dir health (via director's time metric)
* SQL connectivity (via total jobs metric)
## Requirements
* python 3
* python-bareos module
## Installation
1. Configure bareos's profile and user for monitoring (check examples)
2. Install **python-bareos** module (it can be found in official repository since v18 or in pip)
3. Create config at **zabbix_bareos.yml**, set host, user and password:
```
---
host: bareos-dir.example.org
user: zabbix
password: ChangeMe
```
4. Run **bareos.discovery.py** to be sure that all was configured correctly (you should get valid JSON)
5. Put scripts in zabbix-agent scripts dir & set correct permissions
6. Put **userparameter_bareos.conf** in **zabbix_agentd.d** dir and restart agent
7. Import value maps
8. Import template
9. Assign template on host

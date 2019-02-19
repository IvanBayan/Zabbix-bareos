#! /usr/bin/env python2.7
import sys
import bareos.bsock
import argparse
import time
import datetime
import re

host = "bareos-director.local"
user = "zabbix"
password = bareos.bsock.Password("ChangeMe")

def create_console():
    console = bareos.bsock.DirectorConsoleJson(address=host, port=9101, name=user, password=password)
    return console

def last_status(args):
    console = create_console()
    last_job = console.call("llist job={} last".format(args.job))
    print(last_job['jobs'][0]['jobstatus'])

def last_size(args):
    console = create_console()
    last_job = console.call("llist job={} jobstatus=T last".format(args.job))
    print(last_job['jobs'][0]['jobbytes'])

def get_time(args):
    console = create_console()
    dir_time = console.call('time')['time']['full']
    print(int(time.mktime(datetime.datetime.strptime(dir_time,"%a %d-%b-%Y %H:%M:%S").timetuple())))

def get_total_jobs(args):
    console = create_console()
    total_jobs = console.call(".sql query=\"SELECT COUNT(Job) FROM Job;\"")
    try:
        print total_jobs['query'][0]['count']
    except KeyError:
        print(0)

def get_job_estimate(args):
    console = bareos.bsock.DirectorConsole(address=host, port=9101, name=user, password=password)
    # console.send("estimate job={}".format(args.job))
    estimate = console.call("estimate job={}".format(args.job))
    m = re.search('bytes=([0-9,]+)',re.sub(",","", estimate))
    print(int(m.group(1)))




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    last_status_parser = subparsers.add_parser('last_status')
    last_status_parser.add_argument('job')
    last_status_parser.set_defaults(func=last_status)

    last_size_parser = subparsers.add_parser('last_size')
    last_size_parser.add_argument('job')
    last_size_parser.set_defaults(func=last_size)

    get_time_parser = subparsers.add_parser('get_time')
    get_time_parser.set_defaults(func=get_time)

    get_total_jobs_parser = subparsers.add_parser('get_total_jobs')
    get_total_jobs_parser.set_defaults(func=get_total_jobs)

    get_job_estimate_parser = subparsers.add_parser('get_job_estimate')
    get_job_estimate_parser.add_argument('job')
    get_job_estimate_parser.set_defaults(func=get_job_estimate)

    args = parser.parse_args()
    args.func(args)

#!/usr/bin/env python
#
# The MIT License (MIT)
#
# Copyright (c) 2015 Bit9 + Carbon Black
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from cbapi.event import on_event, registry
from cbapi.example_helpers import get_cb_response_object, build_cli_parser
import re
from cbapi.response import sensor_events, event
import sys
import time




class PutAndExecuteJob(object):
    def __init__(self, target,destination):
        self.target = target
        self.destination = destination

    def run(self, session):
       lr_session.put_file(fp,args.w)
       lr_session.create_process(args.f,working_direction=args.w,wait_for_output=False)

def print_result(registry_job):
    try:
        timestamp, sensor_id, registry_key, registry_value = registry_job.result()
    except:
        print("Error encountered when pulling registry key: {0}".format(registry_job.exception()))
    else:
        print("Got result for sensor ID {0} registry key {1}: value is {2}".format(sensor_id, registry_key,
                                                                                   registry_value))


def main():
    parser = build_cli_parser("Push a file to sensors in a fleet")
    args = parser.parse_args()
    parser.add_argument("-q", type=str,help="sensor query",default=None)
    parser.add_argument("-f", type=str,help="file name",default=None)
    parser.add_argument("-w", type=str,help="destination path",default=None)
    cb = get_cb_response_object(args)
    sensors = cb.Select(Sensor).where(args.q) if args.q is not None else cb.select(Sensor).all()
    sensor_ids = [sensor.sensor_id for sensor in sensors]
    fp = open(args.f,"r")
    lrjob = PutAndExecute(args.f,args.w) 







if __name__ == "__main__":
    sys.exit(main())


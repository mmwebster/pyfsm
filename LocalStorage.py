#!/usr/bin/env python

#################################################################################
# Import libraries
#################################################################################
import os
import time
import csv
import os.path
from os import environ as ENV
from datetime import datetime, date, timedelta

#################################################################################
# Perform initializations
#################################################################################


#################################################################################
# Utility functions
#################################################################################

#################################################################################
# Class definitions
#################################################################################
class LocalStorage(object):
    def __init__(self):
        # if not 'PYFSM_TEST_MODE' in ENV or \
        #         not int(ENV['PYFSM_TEST_MODE']) == 1:
        #     # this is REQUIRED...no way to read config before one knows where
        #     # it's located
        #     self.drive_path = "/media/pi/USB-STORAGE"
        # else:
        #     self.drive_path = ENV["LOCAL_STORAGE_PATH"]
        self.drive_path = ENV["LOCAL_STORAGE_PATH"]
        self.ledQueue = ledQueue
        # load values contained in config file
        self.config = {}
        self.load_config_file()
        # load values contained in id-lookup-table file
        self.id_lookup_table = {}
        self.load_id_lookup_table()
        # hash of when the student checked in, if they have
        self.time_in_entries = {}

    # @desc Opens config file, stores all of its key/value pairs, then closes it
    def load_config_file(self):
        try:
            with open(self.drive_path + "/" + "config.csv", 'r') as config_file:
                config_file_reader = csv.reader(config_file)

                for row in enumerate(config_file_reader):
                    self.config[str(row[1][0]).strip()] = str(row[1][1]).strip()
                    print("LS-CONFIG: storing (" + str(row[1][0]).strip() + "," + str(row[1][1]).strip() + ")")
        except:
            # failed to open config file, it's either not present, USB storage
            # device is not plugged in, or it is not named properly
            time.sleep(.9)
            print("ERROR: No USB storage device or configure file")
            print("SYSTEM SHUTTING DOWN")
            if not 'PYFSM_TEST_MODE' in ENV or \
                    not int(ENV['PYFSM_TEST_MODE']) == 1:
                os.system("sudo shutdown now") # fatal error shutdown the system

    def load_id_lookup_table(self):
        with open(self.drive_path + "/" + "id-lookup-table.csv", 'r') as id_file:
            id_file_reader = csv.reader(id_file)

            for row in enumerate(id_file_reader):
                self.id_lookup_table[str(row[1][0]).strip()] = str(row[1][1]).strip()
                print("LS-USER storing (" + str(row[1][0]).strip() + "," + str(row[1][1]).strip() + ")")

    def read_config_value(self, key):
        if key in self.config:
            return self.config[key]
        else:
            return "NOT_FOUND"

    def lookup_id(self, user_id):
        if user_id in self.id_lookup_table:
            return self.id_lookup_table[user_id]
        else:
            return "NOT_FOUND"

    def append_rows(self, file_name, data):
        path = self.drive_path + "/time-entries/" + file_name
        print("Appending rows to path: " + path)
        with open(path, 'ab+') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(data)

    # @desc Get's the user configured time period type for time entries
    #       returns the exact value based on the period. Ex/ if user
    #       configures "time-entry-file-period, by-week" then the
    #       returned value might be "week_2017-4-3" or "week_2017-3-27"
    #       which are both Mondays of their respective weeks
    def get_current_time_period(self):
        # get the config type
        time_period_type = self.read_config_value("time-entry-file-period")
        # branch based on type
        dt = ""
        if time_period_type == "by-hour":
            dt += datetime.now().strftime("hour_%Y-%m-%d_%H_")
        elif time_period_type == "by-day":
            dt += datetime.now().strftime("day_%Y-%m-%d_")
        elif time_period_type == "by-week":
            today = date.today()
            this_monday = today - timedelta(today.weekday())
            dt += this_monday.strftime("week_%Y-%m-%d_")
        elif time_period_type == "by-month":
            dt += datetime.now().strftime("month_%Y-%m_")
        else:
            print("ERROR: invalid value for time-entry-file-period")
            return None
        return dt

#################################################################################
# House keeping..close interfaces and processes
#################################################################################

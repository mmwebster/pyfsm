#!/usr/bin/env python

#################################################################################
# Import libraries
#################################################################################
import time
import csv
from os import environ as ENV

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
    def __init__(self, drive_path):
        self.drive_path = drive_path
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
        with open(self.drive_path + "/" + "config.csv", 'r') as config_file:
            config_file_reader = csv.reader(config_file)

            for row in enumerate(config_file_reader):
                self.config[str(row[1][0]).strip()] = str(row[1][1]).strip()
                print("LS-CONFIG: storing (" + str(row[1][0]).strip() + "," + str(row[1][1]).strip() + ")")

    def load_id_lookup_table(self)
        with open(self.drive_path + "/" + "id-lookup-table.csv", 'r') as id_file:
            id_file_reader = csv.reader(id_file)

            for row in enumerate(id_file_reader):
                self.[str(row[1][0]).strip()] = str(row[1][1]).strip()
                print("LS-USER storing (" + str(row[1][0]).strip() + "," + str(row[1][1]).strip() + ")")

    def read_config_value(self, key):
        if key in self.config:
            return self.config[key]
        else:
            return "NOT_FOUND"

    def lookup_id(self, user_id):
        if user_id in self.user_ids:
            return self.id_lookup_table[user_id]
        else:
            return "NOT_FOUND"

    def append_rows(self, file_name, data):
        if not 'ATTENDANCE_TRACKER_TEST' in ENV or \
                not int(ENV['ATTENDANCE_TRACKER_TEST']) == 1:
            print("Appending rows to path: " + self.drive_path + "/" + file_name)
        with open(self.drive_path + "/" + file_name, 'ab') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(data)

#################################################################################
# House keeping..close interfaces and processes
#################################################################################

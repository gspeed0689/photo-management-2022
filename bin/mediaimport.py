import config
import os
import time
import datetime
import multiprocessing

class Media_Import:
    def __init__(self, source_folder, output_folder="default", importdate="today"):
        self.source_folder = source_folder
        self.import_date = self.import_date(importdate)
        self.output_folder = self.output_folder(output_folder)
        self.staging_folder = self.staging_folder()
        self.import_list = self.list_input_photos()
        pass
    def import_date(self, passed_value):
        if config.timezone == "local":
            today = datetime.datetime(time.localtime()[:6])
        elif config.timezone == "utc":
            today = datetime.datetime(time.gmtime()[:6])
        if passed_value in ["today", "yesterday"]:
            if passed_value == "today":
                return_value = today
            elif passed_value == "yesterday":
                yesterday_timedelta = datetime.timedelta(days=1)
                yesterday = today - yesterday_timedelta
                return_value = yesterday
        return(return_value)
    def output_folder(self, passed_value):
        if passed_value == "default":
            output_folder = 
    def staging_folder(self):
        staging_folder = self.output_folder + os.sep + "staging"
        if os.path.exists(staging_folder) == False:
            os.mkdir(staging_folder)
        return(staging_folder)
    def list_input_photos(self):
        
        pass
    def affinity_bin(self):
        total_cores = multiprocessing.cpu_count()
        active_cores = total_cores - config.affinity_reserve_cores
        active_1s = active_cores * "1"
        inactive_0s = config.affinity_reserve_cores * "0"
        bin_str = f"0b{active_1s}{inactive_0s}"
        hex_str = str(hex(int(bin_str, 2)))[2:]
        return(hex_str)
    def affinity_prefixing(self, prefix, cmd):
        if config.affinity_awareness == True:
            return_list = prefix + cmd
        else:
            return_list = cmd
        return(return_list)
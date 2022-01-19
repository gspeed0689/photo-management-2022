import config
import os
import time
import datetime

class Video:
    def __init__(self, file_path):
        self.filepath = file_path
        self.filename = file_path.split(os.sep)[-1].split(".")[0]
        self.filenametype = file_path.split(os.sep)[-1]
        self.filetype = self.filename.split(".")[-1]
        self.directory = os.path.dirname(file_path)
        self.os_capture_date = self.time2datetime(time.localtime(os.path.getctime(self.filepath)))
    def time2datetime(self, time_obj):
        """Creates a datetime.datetime object from a time object. 

        Args:
            time_obj (time object): Like time.localtime() or time.gmtime()
        """
        datetime_obj = datetime.datetime(*time_obj[:6])
        return(datetime_obj)
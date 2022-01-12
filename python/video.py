import config
import os

class Video:
    def __init__(self, file_path):
        self.filepath = file_path
        self.filename = file_path.split(os.sep)[-1].split(".")[0]
        self.filenametype = file_path.split(os.sep)[-1]
        self.filetype = self.filename.split(".")[-1]
        self.directory = os.path.dirname(file_path)
        pass       
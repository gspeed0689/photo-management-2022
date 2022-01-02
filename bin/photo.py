import config
from mediaUID import MediaUID
import PIL
import os


class Photo:
    def __init__(self, file_path):
        self.filepath = file_path
        self.filename = file_path.split(os.sep)[-1]
        self.filetype = self.filename.split(".")[-1]
        self.uid_method = config.uid_method
        self.uid = self.photo_uid()
        pass
    def photo_uid(self):
        uid = MediaUID(self.filepath).uid
        return(uid)
    def load_exif_data(self):
        pass
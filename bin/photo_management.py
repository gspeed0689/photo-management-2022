#scripts
import config
#non-standard library
from PIL import Image, ExifTags
#standard library
import os
import time
import glob
import shutil
import argparse
import secrets
import uuid
import hashlib
import argparse

class photo_import:
    def __init__(self):
        pass

class photo:
    def __init__(self, file_path):
        self.filepath = file_path
        self.filename = file_path.split(os.sep)[-1]
        self.filetype = self.filename.split(".")[-1]
        self.uid_method = config.uid_method
        self.uid = self.photo_uid()
        pass
    def photo_uid(self):
        self.uid_valid_methods = ["TOKEN", "UUID4", "UUID-4", "HASH-MD5", "HASH-SHA"]
        if self.uid_method == "TOKEN":
            try:
                token_length = config.token_uid_length
            except:
                token_length = 12
            uid = secrets.token_urlsafe(token_length + 10).replace("-", "").replace("_", "")[:12]
        elif self.uid_method.startswith("UUID") == True:
            uid = uuid.uuid4()
            if self.uid_method in "UUID4":
                uid = uid.hex
            else:
                uid = str(uid)
        elif self.uid_method.startswith("HASH"):
            # https://stackoverflow.com/questions/16874598/how-do-i-calculate-the-md5-checksum-of-a-file-in-python
            with open(self.filepath, "rb") as f:
                if self.uid_method.endswith("MD5"):
                    file_hash = hashlib.md5()
                elif self.uid_method.endswith("SHA"):
                    file_hash = hashlib.sha256()
                chunk = f.read(2 ** 13)
                while chunk:
                    file_hash.update(chunk)
                    chunk = f.read(2 ** 13)
            uid = file_hash.hexdigest()
            pass
        else:
            ErrorLine_1 = "The photo uid method set in the config file is not correct."
            ErrorLine_2 = f"{self.uid_method} was provided, possible values should include:"
            ErrorLine_3 = " ".join(self.uid_valid_methods)
            raise ValueError(f"{ErrorLine_1}\n\t{ErrorLine_2}\n\t{ErrorLine_3}")
        return(uid)
    def load_exif_data(self):
        pass

def arguments():
    pass

def main():
    pass

if __name__ == "__main__":
    pass
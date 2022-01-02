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
import multiprocessing
import subprocess

class photo_import:
    def __init__(self, source_folder, output_folder="default"):
        self.source_folder = source_folder
        self.output_folder = output_folder
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

class video:
    def __init__(self, file_path, conversion=True, conversion_method="batch"):
        self.filepath = file_path
        self.filename = file_path.split(os.sep)[-1]
        self.filetype = self.filename.split(".")[-1]
        self.conversion = conversion
        self.conversion_method = conversion_method
        pass
    def conversion_control(self):
        affinity_prefix = ["start", "/affinity", self.affinity_bin()]
        if self.conversion == True:
            if self.conversion_method == "batch":
                pass
            elif self.conversion_method == "subproc":
                pass
        pass
    def affinity_bin(self):
        total_cores = multiprocessing.cpu_count()
        active_cores = total_cores - config.affinity_reserve_cores
        active_1s = active_cores * "1"
        inactive_0s = config.affinity_reserve_cores * "0"
        bin_str = f"0b{active_1s}{inactive_0s}"
        hex_str = str(hex(int(bin_str, 2)))[2:]
        return(hex_str)

def arguments():
    pass

def main():
    pass

if __name__ == "__main__":
    pass
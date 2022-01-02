import config
from mediaUID import MediaUID
import PIL
import os


class Photo:
    def __init__(self, file_path):
        self.filepath = file_path
        self.filename = file_path.split(os.sep)[-1].split(".")[0]
        self.filenametype = file_path.split(os.sep)[-1]
        self.filetype = self.filename.split(".")[-1]
        self.directory = os.path.dirname(file_path)
        self.uid_method = config.uid_method
        self.uid = self.photo_uid()
        self.exif_methods = {"jpg": self.exif_jpg,
                             "cr2": self.exif_cr2,
                             "cr3": self.exif_cr3,
                             "dng": self.exif_dng,
                             "tif": self.exif_tif,
                             "png": self.exif_png,
                             "nef": self.exif_nef,}
        pass
    def photo_uid(self):
        uid = MediaUID(self.filepath).uid
        return(uid)
    def renaming(self):
        naming_structure = f"{self.exif_serial}_{self.uid}_{self.filenametype}"
        return(naming_structure)
    def load_exif_data(self):
        #https://stackoverflow.com/questions/4764932/in-python-how-do-i-read-the-exif-data-for-an-image
        exif_dict = self.exif_methods[self.filetype]()
        self.exif_serial = exif_dict['BodySerialNumber']
        self.exif_brand = exif_dict['Make']
        self.exif_model = exif_dict['Model']
        pass
    def exif_jpg(self):
        pass
    def exif_cr2(self):
        pass
    def exif_cr3(self):
        pass
    def exif_dng(self):
        pass
    def exif_tif(self):
        pass
    def exif_png(self):
        pass
    def exif_nef(self):
        pass
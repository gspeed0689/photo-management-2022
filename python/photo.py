import config
from mediaUID import MediaUID
from PIL import Image, ExifTags
import os
import time
import datetime


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
        """Generates a 'univeral id for a photo, can use many different 
            methods, like a true UUID, a file hash, or a 
            secrets.token_urlsafe() string.

            Developer note: this probably doesn't have to be a 
                separate function. 
        """
        uid = MediaUID(self.filepath).uid
        return(uid)
    def time2datetime(self, time_obj):
        """Creates a datetime.datetime object from a time object. 

        Args:
            time_obj (time object): Like time.localtime() or time.gmtime()
        """
        datetime_obj = datetime.datetime(*time_obj[:6])
        return(datetime_obj)
    def renaming(self):
        """New naming structure of an image file from the camera 
            to a more unique name. 

            Developer note: I use this because my main cameras,
                a pair of Canon M6s offers no in camera name 
                customization. Some days, or series of days, 
                the file names are in conflict, and so Windows
                does its name conflict resolution, and adds (1)
                to the end of the filename. 

                I would rather have a totally unique name to 
                track changes across editing programs, and image
                exports. 
        """
        naming_structure = f"{self.exif_serial}_{self.uid}_{self.filename}"
        return(naming_structure)
    def eliminate_escaped_whitespace(self, input_string):
        """Eliminates whitespace in EXIF Data

        Args:
            input_string (str): String to remove whitespace
        """
        output = input_string
        output = output.replace("\x00", "")
        #output = output.replace("", "")
    def conversion_attempt(self, data):
        """Attempts to convert an EXIF data section to a string

        Args:
            data (any): Data to attempt to convert to string. 
        """
        if type(data) in [bytes, str]:
            try:
                output = data.decode("utf8")
            except:
                output = self.eliminate_escaped_whitespace(data)
            return(output)
        else:
            return(data)
    def load_exif_data(self):
        """Loads EXIF data into self variables.
        """
        #https://stackoverflow.com/questions/4764932/in-python-how-do-i-read-the-exif-data-for-an-image
        exif_dict = self.exif_methods[self.filetype](self.filepath)
        self.exif_serial = exif_dict['BodySerialNumber']
        self.exif_brand = exif_dict['Make']
        self.exif_model = exif_dict['Model']
        pass
    def get_os_shot_time(self):
        """Uses the os library to get the shot time from the file
            system. This is in case the EXIF methods fail. 
        """
        #https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times
        image_time = os.path.getctime(self.filepath)
    def exif_jpg(self):
        """Gathers EXIF data from a JPEG file. 
        """
        load_image = Image.open(self.filepath)
        exif_data = load_image.getexif()
        exif_dict = {ExifTags.TAGS[key]: self.conversion_attempt(value) for (key, value) in exif_data.items()}
        return(exif_dict)
    #The strategy for most of these might be to create tiny JPEGs and then read the exif from that. Let something else read the metadata
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
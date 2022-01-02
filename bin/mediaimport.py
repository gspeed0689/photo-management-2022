from video import Video
from photo import Photo
import config
import os
import time
import datetime
import multiprocessing
import glob
import shutil

class Media_Import:
    def __init__(self, source_folder, output_folder="default", importdate="today"):
        self.source_folder = source_folder
        self.import_date = self.import_date(importdate)
        self.output_folder = self.determine_output_folder(output_folder)
        self.staging_folder = self.determine_staging_folder()
        self.import_list = self.list_input_media()
        self.staging_media_list_evaluation()
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
    def determine_output_folder(self, passed_value):
        if passed_value == "default":
            str_YM = config.folder_date_ym.replace("%Y", self.import_date.year).replace("%m", self.import_date.month).replace("%d", self.import_date.day)
            str_YMD = config.folder_date_ym.replace("%Y", self.import_date.year).replace("%m", self.import_date.month).replace("%d", self.import_date.day)
            fpath0 = config.photo_library + os.sep + str_YM
            fpath1 = fpath0 + os.sep + str_YMD
            self.DC(fpath0)
            self.DC(fpath1)
            output_folder = fpath1
        else: 
            output_folder = passed_value
        return(output_folder)
    def determine_staging_folder(self):
        staging_folder = self.output_folder + os.sep + "staging"
        self.DC(staging_folder)
        return(staging_folder)
    def DC(self, fpath): #Directory Check and Create
        if os.path.exists(fpath) == False:
            os.mkdir(fpath)
    def list_input_media(self):
        media = {"all": []}
        for media_type in config.media_types.keys():
            for file_type in config.media_types[media_type]:
                glob_query_L = self.source_folder + os.sep + f"*.{file_type.lower()}"
                glob_query_U = self.source_folder + os.sep + f"*.{file_type.upper()}"
                glob_results = glob.glob(glob_query_L) + glob.glob(glob_query_U) + []
                if len(glob_results) != 0:
                    media[file_type] = glob_results
                    media["all"] += glob_results
        self.source_media = media
    def move_media_staging(self):
        for infile in self.source_media["all"]:
            filename = infile.split(os.sep[-1])
            outfile = self.staging_folder + os.sep + filename
            shutil.copy2(infile, outfile)
    def staging_media_list_evaluation(self):
        self.staging_media = {key: [x.replace(self.source_folder, self.staging_folder) for x in value] for (key, value) in self.source_media.items()}
        self.staging_videos = {key: [x.replace(self.source_folder, self.staging_folder) for x in value] for (key, value) in self.source_media.items() if key in config.media_types["videos"]}
        self.staging_photos = {key: [x.replace(self.source_folder, self.staging_folder) for x in value] for (key, value) in self.source_media.items() if key in config.media_types["photos"]}
        self.VIDEOS = {key: [Video(x) for x in value] for (key, value) in self.staging_videos}
        self.PHOTOS = {key: [Photo(x) for x in value] for (key, value) in self.staging_photos}
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
    def video_conversion_main(self):
        affinity_prefix = ["start", "/affinity", self.affinity_bin()]
        cmd_list = self.video_commands()
        cmd_list = [self.affinity_prefixing(affinity_prefix, x) for x in cmd_list]
        pass
    def video_commands(self):
        videos = self.VIDEOS
        all_commands = []
        for video in videos:
            out_filename_base = self.output_folder + os.sep + video.filename
            for cmd in config.ffmpeg_video.keys():
                new_cmd = [x.replace("{import_location}", video.filepath).replace("{output_location}", out_filename_base) for x in cmd]
                all_commands.append(new_cmd)
            pass
        pass
    def execute_video_conversion(self):
        if self.conversion == True:
            if self.conversion_method == "batch":
                batch_file_location = self.output_folder + os.sep + "process_video.bat"
                with open(batch_file_location, "w") as f:
                    f.write("")
                pass
            elif self.conversion_method == "subproc":
                pass
        pass
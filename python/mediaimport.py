from video import Video
from photo import Photo
import config
import os
import time
import datetime
import multiprocessing
import subprocess
import glob
import shutil
import platform
###############################################################################
class Media_Import:
    def __init__(self, source_folder, output_folder="default", 
                 importdate="today", 
                 video_conversion=True, 
                 conversion_method="batch", 
                 affinity=False):
        self.source_folder = source_folder
        self.import_date = self.import_date(importdate)
        self.output_folder = self.determine_output_folder(output_folder)
        self.staging_folder = self.determine_staging_folder()
        self.import_list = self.list_input_media()
        self.staging_media_list_evaluation()
        self.conversion = video_conversion
        self.conversion_method = conversion_method
        pass
    def import_date(self, passed_value):
        """Sets the import date of the images to import from the source media

        Args:
            passed_value (str): passed value from the cmd line args for 
                which date to import. 
        """
        if config.timezone == "local":
            today = self.time2datetime(time.localtime())
        elif config.timezone == "utc":
            today = self.time2datetime(time.gmtime())
        if passed_value in ["today", "yesterday"]:
            if passed_value == "today":
                return_value = today
            elif passed_value == "yesterday":
                yesterday_timedelta = datetime.timedelta(days=1)
                yesterday = today - yesterday_timedelta
                return_value = yesterday
        return(return_value)
    def time2datetime(self, time_obj):
        """Creates a datetime.datetime object from a time object. 

        Args:
            time_obj (time object): Like time.localtime() or time.gmtime()
        """
        datetime_obj = datetime.datetime(*time_obj[:6])
        return(datetime_obj)
    def determine_output_folder(self, passed_value):
        """Creates the path and then creates the folder (if necessary) for 
            the current import work. 

        Args:
            passed_value (str): passed value from the cmd line args for
                which date to import.
        """
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
        """Uses the output folder information to create the path string for
            the staging folder, and then creates the staging folder. 
        """
        staging_folder = self.output_folder + os.sep + "staging"
        self.DC(staging_folder)
        return(staging_folder)
    def DC(self, fpath): #Directory Check and Create
        """Checks if a path exists, if not, creates the folder for that path. 

        Args:
            fpath (str): path to check if exists and to create if not. 
        """
        if os.path.exists(fpath) == False:
            os.mkdir(fpath)
    def list_input_media(self):
        """Uses glob.glob() to find the files in the current import folder. 
        """
        media = {"all": []}
        for media_type in config.media_types.keys():
            for file_type in config.media_types[media_type]:
                glob_query_L = self.source_folder + os.sep + f"*.{file_type.lower()}"
                glob_query_U = self.source_folder + os.sep + f"*.{file_type.upper()}"
                glob_results = glob.glob(glob_query_L) + glob.glob(glob_query_U) + []
                if len(glob_results) != 0:
                    media[file_type] = glob_results
                    media["all"] += glob_results
        valid_date_media = [x for x in media if str(self.time2datetime(time.localtime(os.path.getctime(x)))).split(" ")[0] == str(self.import_date).split(" ")[0]]
        self.source_media = valid_date_media
    def move_media_staging(self):
        """Moves the valid import media to the staging folder using 
            shutil.copy2() to preserve file metadata. 
        """
        for infile in self.source_media["all"]:
            filename = infile.split(os.sep[-1])
            outfile = self.staging_folder + os.sep + filename
            shutil.copy2(infile, outfile)
    def staging_media_list_evaluation(self):
        """Dict/List comprehensions to create lists of photos and videos in 
            the current import process."""
        self.staging_media = {key: [x.replace(self.source_folder, self.staging_folder) for x in value] for (key, value) in self.source_media.items()}
        self.staging_videos = {key: [x.replace(self.source_folder, self.staging_folder) for x in value] for (key, value) in self.source_media.items() if key in config.media_types["videos"]}
        self.staging_photos = {key: [x.replace(self.source_folder, self.staging_folder) for x in value] for (key, value) in self.source_media.items() if key in config.media_types["photos"]}
        self.VIDEOS = {key: [Video(x) for x in value] for (key, value) in self.staging_videos}
        self.PHOTOS = {key: [Photo(x) for x in value] for (key, value) in self.staging_photos}
    def affinity_bin(self):
        """Using the total cores of the system, this function will leverage 
            Windows CPU affinity to limit the number of cores subsequent 
            processes can use.
            
            Developer note: I personally use this to keep 4 cores free for 
                other tasks on a 24 thread machine. Really helps with 
                ffmpeg and lightroom. 
        """
        total_cores = multiprocessing.cpu_count()
        active_cores = total_cores - config.affinity_reserve_cores
        active_1s = active_cores * "1"
        inactive_0s = config.affinity_reserve_cores * "0"
        bin_str = f"0b{active_1s}{inactive_0s}"
        hex_str = str(hex(int(bin_str, 2)))[2:]
        return(hex_str)
    def affinity_prefixing(self, prefix, cmd):
        """If affinity prefixing is turned on, it will add an affinity 
            command prefix to a list of commands. 

            This function will return a list for passing to subprocess.run().

            This function will not append an affinity command if the
                platform is not Windows. 

        Args:
            prefix (list): affinity commands list for passing 
                to subprocess.run
            cmd (list): general command list for passing to subprocess.run
        """
        if config.affinity_awareness == True and platform.system == "Windows":
            return_list = prefix + cmd
        else:
            return_list = cmd
        return(return_list)
    def video_conversion_main(self):
        """Creates a list of commands for fmmpeg to convert video. 
        """
        affinity_prefix = ["start", "/affinity", self.affinity_bin()]
        cmd_list = self.video_commands()
        cmd_list = [self.affinity_prefixing(affinity_prefix, x) for x in cmd_list]
        pass
    def video_commands(self):
        """This function will run through each video through each generic 
            command in the config file.  
        """
        videos = self.VIDEOS
        all_commands = []
        for video in videos:
            out_filename_base = self.output_folder + os.sep + video.filename
            for cmd in config.ffmpeg_video.keys():
                new_cmd = [x.replace("{import_location}", video.filepath).replace("{output_location}", out_filename_base) for x in cmd]
                all_commands.append(new_cmd)
            pass
        self.video_command_list = all_commands
    def execute_video_conversion(self):
        """'Executes' each of the video commands for an import process. 

            Execute in this case could be write all the commands to a batch 
                file, or actually pass the commands to subprocess.run().
        """
        cmd_list = self.video_command_list
        if self.conversion == True:
            if self.conversion_method == "batch":
                batch_file_location = f"{self.output_folder}{os.sep}process_video.bat"
                with open(batch_file_location, "w") as f:
                    for cmd in cmd_list:
                        f.write(" ".join(cmd))
            elif self.conversion_method == "subproc":
                self.video_commands_subprocess()
    def video_commands_subprocess(self, cmd_list):
        """Passes a command to subprocess.run() and then checks to see if 
            ffmpeg is still running before passing another command. 

        Args:
            cmd_list (list): list of commands to be passed 
                to subprocess.run().
        """
        process = True
        c = 0
        cmd_max = len(cmd_list)
        while process == True:
            if self.windows_check_process_running("ffmpeg.exe") == True:
                time.sleep(config.conversion_sleep)
            else:
                subprocess.run(cmd_list[c])
                c += 1
                if c > cmd_max:
                    process = False
    def windows_check_process_running(self, process_name):
        """Function from Stack Overflow to check if a process 
            is still running. 

            Developer note: mainly used to check if FFMPEG is still running, 
                if you're using affinity commands you can accidently open   
                hundreds of processes at once. It is a real pain to close 
                that many running commands while they're taking all system 
                memory and calls. 

        Args:
            process_name (str): Process to check if running. 

        Returns:
            bool: True or False if process is running
        """
        #https://stackoverflow.com/questions/7787120/check-if-a-process-is-running-or-not-on-windows
        call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
        # use buildin check_output right away
        output = subprocess.check_output(call).decode()
        # check in last line for process name
        last_line = output.strip().split('\r\n')[-1]
        # because Fail message could be translated
        return last_line.lower().startswith(process_name.lower())
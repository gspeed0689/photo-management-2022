# Photo Management 2022
Photo management scripts for 2022

This is a personal project to automate the import, conversion, and organization of my photography. 

***It is not in a working state at the moment.***

Some features:

* Import via command line from the SD card folder
* Import photos only from today, yesterday, or an ISO 8601 date `YYYY-MM-DD`
* Include a uid in the file name to track exports later
* Multiple uid generation methods
  * secrets.token_urlsafe
  * hashlib.md5
  * hashlib.sha256
  * uuid.uuid4()
* Rename files to avoid duplicate file names  
  * I have two of the same model cameras and there is no way to rename the file prefix in camera. 
  * Will rename to `serial_uid_originalname.ext`
* Convert to DNG
* Create a batch file to convert videos with ffmpeg
* Convert videos using subprocess
* Set affinity for video subprocess conversion (Windows Processor Affinity)
* Run only one affinity enabled process at a time
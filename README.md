# Photo Management 2022
Photo management scripts for 2022

This is a personal project to automate the import, conversion, and organization of my photography. 

***It is not in a working state at the moment.***

Some features:

* Import via command line from the SD card folder
* Import photos only from today or yesterday
* Rename files to avoid duplicate file names  
  * I have two of the same model cameras and there is no way to rename the file prefix in camera. 
* Convert to DNG
* Create a batch file to convert videos with ffmpeg
* Convert videos using subprocess
* Set affinity for video subprocess conversion (Windows Processor Affinity)
* Run only one affinity enabled process at a time
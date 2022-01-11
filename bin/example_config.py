token_uid_length = 12
conversion_sleep = 3
folder_date_ymd = "%Y-%m-%d"
folder_date_ym = "%Y-%m"
photo_library = r""
uid_method = "TOKEN" # TOKEN UUID-4 UUID4 HASH-SHA HASH-MD5
timezone = "local"

imagemagick_location = r""

#affinity commands (for Windows)
affinity_awareness = True
affinity_reserve_cores = 4

#video conversion
ffmpeg_location = r""
ffmpeg_video = {
    #Keys of this dict are suffixes to the output location file names. 
    "libx264": [ffmpeg_location, "-i", "{import_location}", "-c:v", "libx264", "-qscale:v", "2", "{output_location}.mp4"],
    "libx265": [ffmpeg_location, "-i", "{import_location}", "-c:v", "libx265", "-qscale:v", "2", "{output_location}.mkv"],
    "30p_an_libx264": [ffmpeg_location, "-r", "30", "-i", "{import_location}", "-c:v", "libx264", "-qscale:v", "2", "{output_location}.mp4"],
}

media_types = {
    "photos": [".cr2", ".cr3", ".nef", ".dng", ".arw", ".gpr", ".jpg", ".tif"], 
    "videos": [".mp4", ".mov"],
}
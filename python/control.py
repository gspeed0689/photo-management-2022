import config
import argparse

def arg_handler():
    parser = argparse.ArgumentParser(description="Photo import management tool")
    #parser.add_argument("-", "--", help="", default="")
    parser.add_argument("-d", "--date", 
                        help="Date to import, accepts today, yesterday, or an ISO 8601 date.", 
                        default="today")
    parser.add_argument("-o", "--output-folder", 
                        help="", 
                        default="default")
    parser.add_argument("-cv", "--convert-video", 
                        help="convert the video", 
                        default=None)
    parser.add_argument("-dng", "--digital-negative-only", 
                        help="discard the camera, convert and keep only dng", 
                        default=None)
    parser.add_argument("-a", "--affinity", 
                        help="Use processor affinity when converting video, specify a core count if you don't want to use the config or default.", 
                        default=config.affinity_awareness)
    parser.add_argument("-bv", "--batch-video", 
                        help="create a batch file for video conversion", 
                        default=config.affinity_reserve_cores)
    args = parser.parse_args()
    return(args)
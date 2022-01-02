import config
import os
import multiprocessing

class Video:
    def __init__(self, file_path):
        self.filepath = file_path
        self.filename = file_path.split(os.sep)[-1]
        self.filetype = self.filename.split(".")[-1]
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
    def affinity_prefixing(self, prefix, cmd):
        if config.affinity_awareness == True:
            return_list = prefix + cmd
        else:
            return_list = cmd
        return(return_list)
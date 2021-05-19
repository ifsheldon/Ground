from torch.optim.lr_scheduler import _LRScheduler
import json
from bisect import bisect, bisect_right

class MyFileLR(_LRScheduler):

    def __init__(self, optimizer, file_path, last_epoch=-1, verbose=False):
        self.file_path = file_path
        self.read_interval = None
        self.config_dict = {}
        self._update_other_var()

        super(MyFileLR, self).__init__(optimizer, last_epoch, verbose)

    def get_lr(self):
        if not self._get_lr_called_within_step:
            warnings.warn("To get the last learning rate computed by the scheduler, "
                          "please use `get_last_lr()`.", UserWarning)

#         if self.last_epoch == 0 or self.read_interval is None or self.last_epoch & self.read_interval == 0:
#             print("now read")
        self._read_file()
        new_lr = None
        
        for setting_name, setting_dict in self.config_dict.items():
            idx = bisect(setting_dict["steps"], self.last_epoch) - 1
            if setting_name == "learning_rate":
                new_lr = setting_dict["value"][setting_dict["steps"][idx]]
            else:
                setattr(self, setting_name, setting_dict["value"][setting_dict["steps"][idx]])
        
        return [new_lr for group in self.optimizer.param_groups]    
    
    def _update_other_var(self):
        for setting_name, setting_dict in self.config_dict.items():
            idx = bisect(setting_dict["steps"], self.last_epoch) - 1
            if setting_name == "learning_rate":
                pass
            else:
                setattr(self, setting_name, setting_dict["value"][setting_dict["steps"][idx]])
    
    def _read_file(self):
        self.config_dict = {}
        
        with open(self.file_path, "r") as f:
            content = json.load(f)

        # content
#         self.read_interval = int(content["read_interval"])
        for setting_name, step_value_dict in content.items():
            tmp_dict = {int(k):v for k,v in step_value_dict.items()}
            tmp_steps = list(sorted(tmp_dict.keys()))
            self.config_dict[setting_name] = {}
            self.config_dict[setting_name]["steps"] = tmp_steps
            self.config_dict[setting_name]["value"] = tmp_dict
            
        print(self.config_dict)
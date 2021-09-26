import torch
import os
import numpy as np

def normalize_image(img, max_value, min_value):
    if (max_value - min_value)!=0:
        return ((img - min_value) * (1/(max_value - min_value) * 255)).astype('uint8')
    else:
        return img

class MRIDataset:
    def __init__(self, high_res_path, low_res_path, mask_path, filenames=None):
        self.high_res_path = high_res_path
        self.low_res_path = low_res_path
        self.mask_path = mask_path
        self.filenames = filenames

        num_files = len(self.mask_path)

        self.empty=False
        if num_files>0:
            pass
        else:
            self.empty=True

    def __len__(self):
        return len(self.high_res_path)

    def __getitem__(self, item):

        high_res_img = np.load(self.high_res_path[item])
        high_res_img = normalize_image(high_res_img, np.min(high_res_img), np.max(high_res_img))

        low_res_img = np.load(self.low_res_path[item])
        low_res_img = normalize_image(low_res_img, np.min(low_res_img), np.max(low_res_img))

        if self.empty==True:
            mask_img = np.zeros(shape=(24, 24, 24))
        else:
            mask_img = np.load(self.mask_path[item])

        return_dict = {
                "high_res_img": torch.unsqueeze(torch.tensor(high_res_img, dtype=torch.float), 0),
                "low_res_img": torch.unsqueeze(torch.tensor(low_res_img, dtype=torch.float), 0),
                "mask_img": torch.unsqueeze(torch.tensor(mask_img, dtype=torch.float), 0)
            }

        if self.filenames!=None:
            return_dict["filename"] = self.filenames[item]

        return return_dict

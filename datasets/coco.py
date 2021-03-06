import os
import json

from PIL import Image
import numpy as np
from torch.utils.data import Dataset

class CoCoDataset(Dataset):
    def __init__(self, args, split):
        super(CoCoDataset, self).__init__()
        self.args = args
        data_dir = f'data/{self.args.dataset_fullname}'
        label_path = os.path.join(data_dir, f'{self.args.dataset}_label.txt')

        all_labels = [line.strip() for line in open(label_path)]
        self.num_classes = len(all_labels)
        self.label2id = {label:i for i, label in enumerate(all_labels)}

        self.data = []
        name = 'train' if split != 'test' else 'val'
        image_dir = os.path.join(data_dir, f'{name}2014')
        with open(os.path.join(data_dir, f'{self.args.dataset}_{split}.txt'), 'r') as fr:
            for line in fr.readlines():
                image_id, image_label = line.strip().split('\t')
                image_path = os.path.join(image_dir, image_id)
                image_label = [self.label2id[l] for l in image_label.split(',')]
                self.data.append([image_path, image_label])
        # self.data = self.data[:1000]
        self.transform = None

    def __getitem__(self, index):
        image_path, image_label = self.data[index]
        image_data = Image.open(image_path).convert('RGB')
        x = self.transform(image_data)

        # one-hot encoding for label
        y = np.zeros(self.num_classes).astype(np.float32)
        y[image_label] = 1.0
        return x, y
        
    def __len__(self):
        return len(self.data)

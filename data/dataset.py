import os
import logging
import csv
import pandas as pd
from PIL import Image
from torch.utils.data import Dataset

logger = logging.getLogger(__name__)

class Mustard(Dataset):
    def __init__(self, mode, limit=None):
        self.data = self.load_data(mode, limit)
        self.image_ids = list(self.data.keys())
    
    def load_data(self, mode, limit):
        cnt = 0
        data_set = dict()
        if mode in ['train']:
            df = pd.read_csv('data/mustard/'+mode+'_debug_mustard.csv')
            for index, row in df.iterrows():
                if limit != None and cnt >= limit:
                    break

                image = row['image']
                sentence = row['sentence']
                label = row['label']
                image_path = 'data/mustard/img/'+image+'.jpg'

                if os.path.isfile(image_path):
                    data_set[image]={'text':sentence, 'label': label, 'image_path': image_path}
                    cnt += 1
            # with open('data/mustard/'+mode+'_mustard.csv', 'r') as data:
            #     for line in csv.DictReader(data):
            #         if limit != None and cnt >= limit:
            #             break

            #         image = line['image']
            #         sentence = line['sentence']
            #         label = line['label']
            #         image_path = 'mustard/img/'+image+'.jpg'
            
            #         if os.path.isfile(image_path):
            #             data_set[image]={'text':sentence, 'label': label, 'image_path': image_path}
            #             cnt += 1 
        
        if mode in ['test','val']:
            df = pd.read_csv('data/mustard/'+mode+'_debug_mustard.csv')
            for index, row in df.iterrows():
                image = row['image']
                sentence = row['sentence']
                label = row['label']
                image_path = 'data/mustard/img/'+image+'.jpg'

                if os.path.isfile(image_path):
                    data_set[image]={'text':sentence, 'label': label, 'image_path': image_path}
                    cnt += 1
            # with open('data/mustard/'+mode+'_mustard.csv', 'r') as data:
            #     for line in csv.DictReader(data):
            #         image = line['image']
            #         sentence = line['sentence']
            #         label = line['label']
            #         image_path = 'mustard/img/'+image+'.jpg'
            
            #         if os.path.isfile(image_path):
            #             data_set[image]={'text':sentence, 'label': label, 'image_path': image_path}
            #             cnt += 1

        return data_set

    def image_loader(self, id):
        return Image.open(self.data[id]['image_path'])
    
    def text_loader(self, id):
        return self.data[id]['text']

    def __getitem__(self, index):
        id = self.image_ids[index]
        text = self.text_loader(id)
        #text = self.data[id]['text']
        image_feature = self.image_loader(id)
        #image_feature = Image.open(self.data[id]['image_path'])
        label = self.data[id]['label']
        return text, image_feature, label, id

    def __len__(self):
        return len(self.image_ids)
    
    @staticmethod
    def collate_func(batch_data):
        batch_size = len(batch_data)
 
        if batch_size == 0:
            return {}

        text_list = []
        image_list = []
        label_list = []
        id_list = []
        for instance in batch_data:
            text_list.append(instance[0])
            image_list.append(instance[1])
            label_list.append(instance[2])
            id_list.append(instance[3])
        return text_list, image_list, label_list, id_list
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 15:12:57 2021

@Author: RyanHuang
@Notice: 
    写完本代码当事人感觉非常后悔, 写个小小的函数就行, 没必要封装成类hhh
"""

import os
import json
import xml
from tqdm import tqdm
from Format2COCO import ImgAnnItem, X2COCO




class VOCAnnItem(ImgAnnItem):
    # 主要用于 VOC2COCO
    
    def __init__(self, file_path, id_):
        
        super().__init__(file_path, id_)
        self.DOMTree = xml.dom.minidom.parse(file_path)
        self.annotation = self.DOMTree.documentElement
        
        # 图片中标注的数量
        self.ann_num =  len(self.annotation.getElementsByTagName("object"))
        
        self._set_attr()
        
        
    def _set_width_height(self):
        w = int(self.annotation.getElementsByTagName("size")[0].getElementsByTagName("width")[0].childNodes[0].data)
        h = int(self.annotation.getElementsByTagName("size")[0].getElementsByTagName("height")[0].childNodes[0].data)
        self.img_wh = [w, h]
        
    def _set_file_name(self):
        self.file_name = self.annotation.getElementsByTagName("filename")[0].childNodes[0].data
        
    def _set_xyxy(self): # VOC
        self.xyxy = []
        for i in range(self.ann_num):
            xmin = int(self.annotation.getElementsByTagName("object")[i].getElementsByTagName("bndbox")[0].getElementsByTagName("xmin")[0].childNodes[0].data)
            xmax = int(self.annotation.getElementsByTagName("object")[i].getElementsByTagName("bndbox")[0].getElementsByTagName("xmax")[0].childNodes[0].data)
            ymin = int(self.annotation.getElementsByTagName("object")[i].getElementsByTagName("bndbox")[0].getElementsByTagName("ymin")[0].childNodes[0].data)
            ymax = int(self.annotation.getElementsByTagName("object")[i].getElementsByTagName("bndbox")[0].getElementsByTagName("ymax")[0].childNodes[0].data)
            self.xyxy.append([xmin, ymin, xmax, ymax])
        
    def _set_xywh(self): # COCO
        self.xywh = []
        for xyxy in self.xyxy:
            xmin, ymin, xmax, ymax = xyxy
            x, y, w, h = xmin, ymin, xmax-xmin, ymax-ymin
            self.xywh.append([x, y, w, h])
        
    def _set_type(self):
        self.type_ = []
        for i in range(self.ann_num):
            type_ = self.annotation.getElementsByTagName("object")[i].getElementsByTagName("name")[0].childNodes[0].data
            self.type_.append(type_)
            
    def _set_attr(self):
        self._set_width_height()
        self._set_file_name()
        self._set_type()
        self._set_xyxy()
        self._set_xywh()



class VOC2COCO(X2COCO):
    
    def __init__(self, voc_files_root, save_path=None):
        
        # 一般来说, 该目录下有一堆XML标注文件
        super().__init__(voc_files_root)
        self.file_list = os.listdir(self.root_path)
        self.file_list = [os.path.join(self.root_path, file) for file in self.file_list]
        
        self.type_list = []
        
        self.images = []
        self.annotations = []
        self.categories = []
        
        self.global_ann_idx = 0
        self.go()
        if save_path is None:
            pass
        else:
            with open(save_path, 'w', encoding="UTF-8") as fp:
                json.dump(self.json_format, fp)
        
        
    def go(self):
        
        for id_, file in tqdm(enumerate(self.file_list)):
            ann_item = VOCAnnItem(file, id_)
            
            for i in range(ann_item.ann_num):
                
                img_ann = {}
                img_ann["width"] = ann_item.img_wh[0]
                img_ann["height"] = ann_item.img_wh[1]
                img_ann["file_name"] = ann_item.file_name
                img_ann["id"] = id_
                self.images.append(img_ann)
                
                ann_dic = {
                    "segmentation": [],
                    "bbox": ann_item.xywh[i],
                    "category_id": ann_item.type_[i],
                    "image_id": id_,
                    "id": self.global_ann_idx,
                    "area": ann_item.xywh[i][2]*ann_item.xywh[i][3],
                }
                self.annotations.append(ann_dic)
                self.type_list += ann_item.type_
                self.global_ann_idx += 1


        self.type_list = list(set(self.type_list))
        self._set_type2id(self.type_list)
        
        for type_, id_ in self.type2id.items():
            category = {
                    "supercategory": "none",
                    "name": type_,
                    "id": id_
                }
            self.categories.append(category)
        
        
        for idx, ann in enumerate(self.annotations):
            self.annotations[idx]["category_id"] = self.type2id[ann["category_id"]]
            
        self.json_format = {
            "images":self.images,
            "annotations":self.annotations,
            "categories":self.categories,
            }

        

if __name__ == "__main__":
    # 将 F:\CCFxunlian\Annotations 下的标注整成 F:\CCFxunlian\COCO.json
    VOC2COCO(r'F:\CCFxunlian\Annotations', r'F:\CCFxunlian\COCO.json')
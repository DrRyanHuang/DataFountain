# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 15:57:04 2021

@author: Ryan
"""

class ImgAnnItem:
    # 主要用于 VOC2COCO
    
    def __init__(self, file_path, id_):
        self.file_path = file_path
        self.id_ = id_
        
    def _set_width_height(self):
        self.img_wh = [0, 0]
    def _set_file_name(self):
        self.file_name = ''
    def _set_xyxy(self): # VOC
        self.xyxy = [0, 0, 0, 0]
    def _set_xywh(self): # COCO
        self._set_xywh = [0, 0, 0, 0]
    def _set_type(self):
        self.type_ = None
        
        
class X2COCO:
    
    def __init__(self, root_path):
        self.root_path = root_path
        
    def _set_type2id(self, type_list):
        self.type2id = {k:v for v,k in enumerate(type_list)}
    
    def _set_id2type(self, type_list):
        self.id2type = {k:v for k,v in enumerate(type_list)}
import sys
import time
import serial  # 这个模块是通信模块
# from testObject  import *
import matplotlib
matplotlib.use('Agg')
import os
from keras.models import load_model
import numpy as np
from PIL import Image
import cv2
import tensorflow as tf
from enum import Enum

# global graph
# graph = tf.get_default_graph() 
gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.333)
 
sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))



class NN(Enum):
    Instance=()
    def __init__(self):
        # super().__init__()
        self.model1 = load_model(".\model\inc_checkpoint-1507-1.00-0.9854166666666667-0.004233809653669596-0.06068343079338471.hdf5")
        self.model2 = load_model(".\model\inc_checkpoint2-1375-1.00-0.9166666666666666-0.02896706387400627-0.23649475624163946.hdf5")
        global graph
        graph = tf.get_default_graph() 
        
    def get_inputs(self,src=[]):
        pre_x = []
        for s in src:
            input = cv2.imread(s)
            input = cv2.resize(input, (300, 300))
            input = cv2.cvtColor(input, cv2.COLOR_BGR2RGB)
            pre_x.append(input)  # input一张图片
        pre_x = np.array(pre_x) / 255.0
        return pre_x
        
    def JudgeGesture(self):
        #model路径
        #要预测的图片保存在这里
        predict_dir = './data'
        #这个路径下有两个文件，分别是cat和dog
        test = os.listdir()
        images = []
        #获取每张图片的地址，并predict_dir保存在列表images中
        for fn in os.listdir(predict_dir):
            if fn.startswith('test') and fn.endswith('jpg'):#名字可能要修改i
                fd = os.path.join(predict_dir,fn)
                print(fd)
                images.append(fd)
        #调用函数，规范化图片
        pre_x = self.get_inputs(images)
        #预测
        with graph.as_default():
            pre_y_1 = self.model1.predict(pre_x)
            pre_y_2 = self.model2.predict(pre_x)
        max_index=np.argmax(pre_y_1+pre_y_2)
        
        gesture_num = max_index%6+1
        if gesture_num == 1:
            gesture_action = 1
            print('This is a eletronic with possibility model1:%.6f model2:%.6f' % (pre_y_1[:,0],pre_y_2[:,0]))
            # self.result_show_1()
        elif gesture_num == 2:
            gesture_action = 2
            print('This is a glass with possibility %.6f model2:%.6f' % (pre_y_1[:,1],pre_y_2[:,1]))
            # self.result_show_2()
        elif gesture_num == 3:
            gesture_action = 3
            print('This is a metal with possibility %.6f  model2:%.6f' % (pre_y_1[:,2],pre_y_1[:,2]))
            # self.result_show_3()
        elif gesture_num == 4:
            gesture_action = 4
            print('This is a paper with possibility %.6f  model2:%.6f' % (pre_y_1[:,3],pre_y_2[:,3]))
            # self.result_show_4()
        elif gesture_num == 5:
            gesture_action = 5
            print('This is a plastic with possibility %.6f  model2:%.6f' % (pre_y_1[:,4],pre_y_2[:,4]))
            # self.result_show_5()
        elif gesture_num == 6:
            gesture_action = 6
            print('This is a trash with possibility %.6f  model2:%.6f' %(pre_y_1[:,5],pre_y_2[:,5]))
            # self.result_show_6()
        return gesture_action
    
Test = NN.Instance
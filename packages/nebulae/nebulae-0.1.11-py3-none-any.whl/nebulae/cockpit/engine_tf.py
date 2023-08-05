#!/usr/bin/env python
'''
engine_tf
Created by Seria at 04/02/2019 4:31 PM
Email: zzqsummerai@yeah.net

                    _ooOoo_
                  o888888888o
                 o88`_ . _`88o
                 (|  0   0  |)
                 O \   。   / O
              _____/`-----‘\_____
            .’   \||  _ _  ||/   `.
            |  _ |||   |   ||| _  |
            |  |  \\       //  |  |
            |  |    \-----/    |  |
             \ .\ ___/- -\___ /. /
         ,--- /   ___\<|>/___   \ ---,
         | |:    \    \ /    /    :| |
         `\--\_    -. ___ .-    _/--/‘
   ===========  \__  NOBUG  __/  ===========
   
'''
# -*- coding:utf-8 -*-
import tensorflow as tf
from ..toolkit.utility import getAvailabelGPU

class EngineTF(object):
    '''
    Param:
    device: 'gpu' or 'cpu'
    available_gpus
    gpu_mem_fraction
    if_conserve
    least_mem
    '''
    def __init__(self, param):
        self.param = param
        # look for available gpu devices
        self.config_proto = tf.ConfigProto(log_device_placement=False)
        self.config_proto.gpu_options.allow_growth = self.param['if_conserve']
        if self.param['device'].lower() == 'gpu':
            self.config_proto.gpu_options.per_process_gpu_memory_fraction = self.param['gpu_mem_fraction']
            if not self.param['available_gpus']:
                gpus = getAvailabelGPU(self.param['least_mem'])
                if gpus < 0:
                    raise Exception('No available gpu', gpus)
                gpus = str(gpus)
            else:
                gpus = self.param['available_gpus']
            self.config_proto.gpu_options.visible_device_list = gpus
            print('+' + ((24 + len(gpus)) * '-') + '+')
            print('| Reside in Device: \033[1;36mGPU-%s\033[0m |' % gpus)
            print('+' + ((24 + len(gpus)) * '-') + '+')
        elif self.param['device'].lower() == 'cpu':
            print('+' + (23 * '-') + '+')
            print('| Reside in Device: \033[1;36mCPU\033[0m |')
            print('+' + (23 * '-') + '+')
        else:
            raise KeyError('Given device should be either cpu or gpu.')
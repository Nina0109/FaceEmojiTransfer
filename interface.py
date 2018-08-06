import os
import sys
import argparse
from solver import Solver
from data_loader import get_loader
from torch.backends import cudnn
from torch.utils import data
from torchvision import transforms as T
from torchvision.utils import save_image
from torchvision.datasets import ImageFolder
from PIL import Image
import torch
import random
import numpy as np
import time
import datetime
def str2bool(v):
    return v.lower() in ('true')

class Gan:
    def __init__(self, config):
        # Model configuration.
        self.config = config
        self.config.c_dim = 4
        self.config.c2_dim = 4
        self.config.celeba_crop_size = 178
        self.config.rafd_crop_size = 600  # my modified final:512/ 600_final
        self.config.image_size=128
        self.config.g_conv_dim =64
        self.config.d_conv_dim =64
        self.config.g_repeat_num =6
        self.config.d_repeat_num =6
        self.config.lambda_cls =1
        self.config.lambda_rec =10
        self.config.lambda_gp =10

        # Training configuration.
        self.config.dataset = 'RaFD'
        self.config.batch_size = 16
        self.config.num_iters = 200000
        self.config.num_iters_decay = 100000
        self.config.g_lr = 0.0001
        self.config.d_lr = 0.0001
        self.config.n_critic = 5
        self.config.beta1 = 0.5
        self.config.beta2 = 0.999
        self.config.resume_iters = None
        self.config.selected_attrs =['Black_Hair', 'Blond_Hair', 'Brown_Hair', 'Male', 'Young']

        # Test configuration.
        self.config.test_iters = 200000



        # Miscellaneous.
        self.config.num_workers = 1
        self.config.mode = 'train' 
        self.config.use_tensorboard = False

        # Directories.
        self.config.celeba_image_dir = '/data/users/zhenju/01_Project/06_Gan/StarGAN/data/CelebA_nocrop/images'
        self.config.attr_path = '/data/users/zhenju/01_Project/06_Gan/StarGAN/data/list_attr_celeba.txt'
        self.config.rafd_image_dir = '/data/users/zhenju/01_Project/06_Gan/StarGAN/data/RaFD/train'
        self.config.log_dir = '/data/users/zhenju/01_Project/06_Gan/StarGAN/stargan/logs'
        #self.config.model_save_dir = 'stargan_rafd/models'
        self.config.model_save_dir = '/data/users/zhenju/01_Project/06_Gan/StarGAN/guancheng_model/'
        self.config.sample_dir = '/data/users/zhenju/01_Project/06_Gan/StarGAN/stargan/samples'
        self.config.result_dir = '/data/users/zhenju/01_Project/06_Gan/StarGAN/stargan/results'

        # Step size.
        self.config.log_step = 10
        self.config.sample_step = 1000
        self.config.model_save_step = 10000
        self.config.lr_update_step = 1000
        if not os.path.exists(self.config.log_dir):
            os.makedirs(self.config.log_dir)
        if not os.path.exists(self.config.model_save_dir):
            os.makedirs(self.config.model_save_dir)
        if not os.path.exists(self.config.sample_dir):
            os.makedirs(self.config.sample_dir)
        if not os.path.exists(self.config.result_dir):
            os.makedirs(self.config.result_dir)
        celeba_loader = None
        rafd_loader = None
        self.Solver = Solver(celeba_loader, rafd_loader, self.config)
	
        self.transform = []
        self.transform.append(T.CenterCrop(self.config.rafd_crop_size))
        self.transform.append(T.Resize(self.config.image_size))
        self.transform.append(T.ToTensor())
        self.transform.append(T.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5)))
        self.transform = T.Compose(self.transform)
        self.Solver.restore_model(self.config.test_iters)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def GanImage(self, filepath):
        image = Image.open(filepath)
        x_real = self.transform(image)
        x_real.resize_(1,3,128,128) 
        c_trg_list = []
        with torch.no_grad():
            x_real = x_real.to(self.device)
            #c_trg_list = self.create_labels(c_org, self.c_dim, self.dataset, self.selected_attrs)
            c_trg_clone=torch.FloatTensor(np.zeros((1,4)))
            for i in range(4):
                c_trg = c_trg_clone.clone()
                c_trg[0, i] = 1
                c_trg_list.append(c_trg.to(self.device))
                # Translate images.
            x_fake_list = [x_real]
            for c_trg in c_trg_list:
                print(x_real.size())
                x_fake_list.append(self.Solver.G(x_real, c_trg))
            return x_fake_list
def denorm(x):
    out = (x + 1) / 2
    return out.clamp_(0, 1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    config = parser.parse_args()
    gan=Gan(config)
    #lists=gan.GanImage("WechatIMG11.jpeg")
    #lists=gan.GanImage("WechatIMG12.jpeg")
    #lists=gan.GanImage("/data/users/yiweizhu/1.jpg")
    lists=gan.GanImage("static/uploaded_images/test.jpg")
    PROCESSED_FOLDER = './static/processed_images/'
    for i in range(len(lists)):
        save_image(denorm(lists[i].data.cpu()), PROCESSED_FOLDER + str(i) + ".jpg", nrow=1, padding=0)

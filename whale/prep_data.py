#prepare dataset
import os
import multiprocessing
import collections
from skimage import transform
import cv2
import numpy as np
from whale_localizer import find_whale
import mxnet as mx


def prep_train_list(train_csv, out_path):
    '''
    make the image list
    according to this tutorial:
    http://mxnet.readthedocs.org/en/latest/python/io.html
    also returns {img_name: whale_id} dictionary
    '''
    f = open(train_csv)
    f.next()
    out_dict = {}
    out_f = open(out_path, 'w')
    ind = 0
    for line in f:
        img_name, whale_id = line.strip().split(',')
        out_dict[img_name.split('.')[0]] = whale_id.split('_')[1]
        out_f.write("{}\t{}\t{}_1.jpg\n".format(ind, whale_id.split('_')[1], img_name.split('.')[0]))
        ind += 1
        out_f.write("{}\t{}\t{}_2.jpg\n".format(ind, whale_id.split('_')[1], img_name.split('.')[0]))
        ind += 1
    f.close()
    return out_dict


def sub_train_list(train_csv, sub_out, top_n = 10):
    '''
    extract top_n most common whales, write to sub_out
    '''
    out_f = open(sub_out, 'w')
    out_f.write("Image,whaleID\n")
    with open(train_csv) as fin:
        all_line = fin.readlines()
        whale_id = [line.strip().split(',')[1] for line in all_line][1:] # [1:] remove header
        whale_img = [line.strip().split(',')[0] for line in all_line][1:]
    whale_cnt = collections.Counter(whale_id)  
    top_id = [it for it, _ in whale_cnt.most_common(top_n)]
    print len(whale_id), len(whale_img)
    for ind, _id in enumerate(whale_id):
        if _id in top_id:
            out_f.write("{},{}\n".format(whale_img[ind], _id))


def prep_train_img(img_dir, img_name, output_dir, resize_shape):
    '''
    prepare trainning data
    resize_shape[0] < resize_shape[1] 
    '''
    img_path = os.path.join(img_dir,"{}.jpg".format(img_name))
    print img_path
    img = find_whale(img_path)
    height, width, _ = img.shape
    if height > width:
        img_1 = transform.rotate(img, 90, resize=True, preserve_range=True)
        img_1 = transform.resize(img_1, resize_shape, preserve_range=True)
        img_2 = transform.rotate(img, 270, resize=True, preserve_range=True)
        img_2 = transform.resize(img_2, resize_shape, preserve_range=True)
    else:
        img_1 = img
        img_1 = transform.resize(img_1, resize_shape, preserve_range=True)
        img_2 = transform.rotate(img, 180, resize=True, preserve_range=True)
        img_2 = transform.resize(img_2, resize_shape, preserve_range=True)
    cv2.imwrite(os.path.join(output_dir, "{}_1.jpg".format(img_name)), img_1)
    cv2.imwrite(os.path.join(output_dir, "{}_2.jpg".format(img_name)), img_2)


def prep_mxnet_data(train_dir, img_list):
    '''
    integrate from mxnet/tools/im2rec.py
    '''
    record = mx.recordio.MXRecordIO(os.path.join(train_dir, 'whale_train.rec'), 'w')
    with open(img_list) as fin:
        for line in fin.readlines():
            line = [i.strip() for i in line.strip().split('\t')]
            item = [int(line[0])] + [line[-1]] + [float(i) for i in line[1:-1]]
            header = mx.recordio.IRHeader(0, item[2], item[0], 0)
            img = cv2.imread(os.path.join(train_dir, item[1]))
            s = mx.recordio.pack_img(header, img, quality=80, img_fmt=".jpg")
            record.write(s)


    



if __name__ == '__main__':
    import sys
    config = sys.argv[1]
    if config == "luyi_mbp":
        raw_data_dir = "/Users/luyi/Dropbox/noaa_kaggle/data/imgs"
        train_csv = "/Users/luyi/git/PicDL/resource/train.csv"
        sub_train_csv = "/Users/luyi/git/PicDL/resource/sub_train.csv"
        submit_csv = "/Users/luyi/Dropbox/noaa_kaggle/data/sample_submission.csv"
        train_dir = "/Users/luyi/Dropbox/noaa_kaggle/data/train"
        nct = 8
    elif config == "luyi_cloud":
        raw_data_dir = "/home/tlytiger/raw_data/imgs"
        train_csv = "/home/tlytiger/PicDL/resource/train.csv"
        #submit_csv = "/Users/luyi/Dropbox/noaa_kaggle/data/sample_submission.csv"
        train_dir = "/home/tlytiger/train_data"
        nct = 2
    sub_train_list(train_csv, sub_train_csv)
    img_list = os.path.join(train_dir, "whale_train.lst")
    train_dict = prep_train_list(sub_train_csv, img_list)
    resize_shape = (224,224)
    pool = multiprocessing.Pool(processes=nct)
    for key in train_dict:
        #print key
        #prep_train_img(raw_data_dir, key, train_dir, resize_shape)
        pool.apply_async(prep_train_img, (raw_data_dir, key, train_dir, resize_shape))
    pool.close()
    pool.join()
    prep_mxnet_data(train_dir, img_list)
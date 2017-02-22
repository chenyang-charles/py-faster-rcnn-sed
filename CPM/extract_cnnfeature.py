import sys
import os.path
import argparse

import numpy as np
from scipy.misc import imread, imresize, imsave
import scipy.io

import cPickle as pickle
from os import walk
import string

caffepath = '/mnt/sdc/chenyang/convolutional-pose-machines-release/caffe/python/'
sys.path.append(caffepath)
import caffe


def predict(in_data, net):
    """
    Get the features for a batch of data using network

    Inputs:
    in_data: data batch
    """
    
    out = net.forward(**{net.inputs[0]: in_data})
    #print out[net.outputs[0]].shape
    features = out[net.outputs[0]]#.squeeze(axis=(2,3))
    return features


def resize(img, H, W):
    """
    Firstly, resize the minimal edge to 256,
    then resize maximal edge to keep ratio,
    finally, choose a H * W subimage from the center
    """
    if img.shape[0] < img.shape[1]:
            width = img.shape[1] * 256 / img.shape[0]
            img = imresize(img, (256, width), 'bicubic')
            row = (256 - H) / 2
            col = (width - W) / 2
            img = img[row : row + H, col : col + W]
    else:
            height = img.shape[0] * 256 / img.shape[1]
            img = imresize(img, (height, 256), 'bicubic')
            row = (height - H) / 2
            col = (256 - W) / 2
            img = img[row : row + H, col : col + W]

    return img


H = 0
W = 0

def batch_predict(filenames, net):
    """
    Get the features for all images from filenames using a network

    Inputs:
    filenames: a list of names of image files

    Returns:
    an array of feature vectors for the images in that file
    """

    global H
    global W

    N, C, H, W = net.blobs[net.inputs[0]].data.shape
    F = net.blobs[net.outputs[0]].data.shape[1]
    Nf = len(filenames)
    Hi, Wi, _ = imread(filenames[0]).shape
    allftrs = np.zeros((Nf, F, 13, 13))
    for i in range(0, Nf, N):
        in_data = np.zeros((N, C, H, W), dtype=np.float32)

        batch_range = range(i, min(i+N, Nf))
        batch_filenames = [filenames[j] for j in batch_range]
        Nb = len(batch_range)

        batch_images = np.zeros((Nb, 3, H, W))
        for j,fname in enumerate(batch_filenames):
            im = imread(fname)
            # If it's grey img
            if len(im.shape) == 2:
                    im = np.tile(im[:,:,np.newaxis], (1,1,3))
            # RGB -> BGR
            im = im[:,:,(2,1,0)]
            # mean subtraction
            im = im - np.array([103.939, 116.779, 123.68])
            # resize
            #im = imresize(im, (H, W), 'bicubic')
            im = resize(im, H, W)
            # get channel in correct dimension
            im = np.transpose(im, (2, 0, 1))
            batch_images[j,:,:,:] = im

        # insert into correct place
        in_data[0:len(batch_range), :, :, :] = batch_images

        # predict features
        ftrs = predict(in_data, net)

        for j in range(len(batch_range)):
                allftrs[i+j,:,:,:] = ftrs[j,:,:,:]

        print 'Done %d/%d files' % (i+len(batch_range), len(filenames))


    return allftrs


"""
	Main
"""


if __name__ == '__main__':

    caffe.set_mode_gpu()
    model_def = 
    model = 
    net = caffe.Net(args.model_def, args.model, caffe.TEST)

    filenames = []
    for (dirpath, dirname, files) in walk(args.files):
        for i in range(0, len(files)):
            filename = os.path.join(dirpath, files[i])
            if string.find(filename, ".jpg") != -1:
                filenames.append(filename)

    mat = batch_predict(filenames, net)

    """
    if args.out:
        # store the features in a pickle file
        with open(args.out, 'w') as fp:
            pickle.dump(allftrs, fp)

    #scipy.io.savemat(os.path.join(base_dir, 'vgg_feats.mat'), mdict =	{'feats': np.transpose(allftrs)})
    """

    maxImgs = []

    for i in range(0, mat.shape[1]):
        activation = sorted(list(np.ndenumerate(mat[:, i, :, :])), key=lambda x:x[1], reverse=True)
        maxImg = [val[0] for val in activation]
        maxImgs.append(maxImg)

    for i in range(0, len(maxImgs)):
        for j in range(0, 5):
            RF = theoreticRF(maxImgs[i][j], 163, 5, filenames[maxImgs[i][j][0]])
            imsave("RFs/pool5/" + str(i) + "_" + str(j) + ".jpg", RF)

        print i, "/", len(maxImgs), "finished"



from PIL import Image
import numpy as np
from scipy.spatial import distance
import pickle
import scipy.spatial.distance as distance
from cyvlfeat.sift.dsift import dsift
from time import time
import cv2

def get_bags_of_sifts(image_paths):
    ############################################################################
    # TODO:                                                                    #
    # This function assumes that 'vocab.pkl' exists and contains an N x 128    #
    # matrix 'vocab' where each row is a kmeans centroid or visual word. This  #
    # matrix is saved to disk rather than passed in a parameter to avoid       #
    # recomputing the vocabulary every time at significant expense.            #
    #                                                                          #                                                               
    # image_feats is an N x d matrix, where d is the dimensionality of the     #
    # feature representation. In this case, d will equal the number of clusters#
    # or equivalently the number of entries in each image's histogram.         #
    #                                                                          #
    # You will construct SIFT features here in the same way you did in         #
    # build_vocabulary (except for possibly changing the sampling rate)        #
    # and then assign each local feature to its nearest cluster center         #
    # and build a histogram indicating how many times each cluster was used.   #
    # Don't forget to normalize the histogram, or else a larger image with more#
    # SIFT features will look very different from a smaller version of the same#
    # image.                                                                   #
    ############################################################################
    '''
    Input : 
        image_paths : a list(N) of training images
    Output : 
        image_feats : (N, d) feature, each row represent a feature of an image
    '''
    fh = open('vocab.pkl', 'rb')
    vocab = pickle.load(fh)
    step_sample = 1
    #print("step_sample", step_sample)
    image_feats = []
    i=-1
    for path in image_paths:
        i+=1
        #if (not i%20):
        #    print(" i = ", i)
        img = cv2.imread(path)
        img2D = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        frames, descriptors = dsift(img2D, step=[step_sample,step_sample], window_size=4, fast=True)
        descriptors =descriptors[::5]
        #histogram
        #for each img:
        #    for each feature: (may different)
        #        find closet feature from vocab 
        dist = distance.cdist(vocab, descriptors)  
        kmin = np.argmin(dist, axis = 0)
        hist, bin_edges = np.histogram(kmin, bins=len(vocab))
        hist_norm = [float(i)/sum(hist) for i in hist]
        image_feats.append(hist_norm)
    image_feats = np.matrix(image_feats)
    #print("image_feats.shape", image_feats.shape)
    #############################################################################
    #                                END OF YOUR CODE                           #
    #############################################################################
    return image_feats

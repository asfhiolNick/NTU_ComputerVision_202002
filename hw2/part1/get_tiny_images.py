from PIL import Image
import numpy as np
import cv2

def get_tiny_images(image_paths):
    #############################################################################
    # TODO:                                                                     #
    # To build a tiny image feature, simply resize the original image to a very #
    # small square resolution, e.g. 16x16. You can either resize the images to  #
    # square while ignoring their aspect ratio or you can crop the center       #
    # square portion out of each image. Making the tiny images zero mean and    #
    # unit length (normalizing them) will increase performance modestly.        #
    #############################################################################
    '''
    Input : 
        image_paths: a list(N) of string where each string is an image 
        path on the filesystem.
    Output :
        tiny image features : (N, d) matrix of resized and then vectorized tiny
        images. E.g. if the images are resized to 16x16, d would equal 256.
    '''
    tiny_images = []
    for path in image_paths:
        img = cv2.imread(path)
        img2D = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        tiny_img2D = cv2.resize(img2D, (16, 16), interpolation=cv2.INTER_AREA)
        tiny_img1D = tiny_img2D.flatten()
        tiny_images.append(tiny_img1D)

    tiny_images = np.matrix(tiny_images)     
    #print(tiny_images.shape)  
    ##############################################################################
    #                                END OF YOUR CODE                            #
    ##############################################################################

    return tiny_images

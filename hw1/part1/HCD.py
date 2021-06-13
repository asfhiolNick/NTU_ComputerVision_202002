import numpy as np
import cv2
import matplotlib.pyplot as plt
import copy


class Harris_corner_detector(object):
    def __init__(self, threshold):
        self.threshold = threshold

    def detect_harris_corners(self, img):
        ### TODO ####
        # Step 1: Smooth the image by Gaussian kernel
        # - Function: cv2.GaussianBlur (kernel = 3, sigma = 1.5)
        img = cv2.GaussianBlur(img, (3,3), 1.5)
        
        # Step 2: Calculate Ix, Iy (1st derivative of image along x and y axis)
        # - Function: cv2.filter2D (kernel = [[1.,0.,-1.]] for Ix or [[1.],[0.],[-1.]] for Iy)
        Ix = cv2.filter2D(img, -1, np.array([[1.,0.,-1.]]) )
        Iy = cv2.filter2D(img, -1, np.array([[1.],[0.],[-1.]]) )
        
        # Step 3: Compute Ixx, Ixy, Iyy (Ixx = Ix*Ix, ...)
        Ixx = Ix*Ix
        Ixy = Ix*Iy
        Iyy = Iy*Iy
        
        # Step 4: Compute Sxx, Sxy, Syy (weighted summation of Ixx, Ixy, Iyy in neighbor pixels)
        # - Function: cv2.GaussianBlur (kernel = 3, sigma = 1.)
        Sxx = cv2.GaussianBlur(Ixx, (3,3), 1.)
        Sxy = cv2.GaussianBlur(Ixy, (3,3), 1.)
        Syy = cv2.GaussianBlur(Iyy, (3,3), 1.)
        
        # Step 5: Compute the det and trace of matrix M (M = [[Sxx, Sxy], [Sxy, Syy]])
        M = np.stack((np.stack((Sxx,Sxy), axis=2), np.stack((Sxy,Syy), axis=2)), axis=3)
        det = np.linalg.det(M)
        trace = np.trace(M, axis1=2, axis2=3)
        
        # Step 6: Compute the response of the detector by det/(trace+1e-12)
        response = np.divide(det, (trace+1e-12))
        return response
    
    def post_processing(self, response):
        ### TODO ###
        # Step 1: Thresholding
        # Step 2: Find local maximum
        local_max = []
        response = np.pad(response, ((2,2),(2,2)), 'constant')
        for i in range(2, response.shape[0]-2):
            for j in range(2, response.shape[1]-2):
                portion = copy.deepcopy(response[i-2:i+3, j-2:j+3])
                portion[2,2]=-1
                if response[i,j]>self.threshold and response[i,j]>np.amax(portion):
                    local_max.append([i-2, j-2])

        return local_max
import numpy as np
import cv2
import random
from tqdm import tqdm
from utils import solve_homography, warping

random.seed(999)

def panorama(imgs):
    """
    Image stitching with estimated homograpy between consecutive
    :param imgs: list of images to be stitched
    :return: stitched panorama
    """
    h_max = max([x.shape[0] for x in imgs])
    w_max = sum([x.shape[1] for x in imgs])

    # create the final stitched canvas
    dst = np.zeros((h_max, w_max, imgs[0].shape[2]), dtype=np.uint8)
    dst[:imgs[0].shape[0], :imgs[0].shape[1]] = imgs[0]
    last_best_H = np.eye(3)
    out = None

    w = 0
    orb = cv2.ORB_create()
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    # for all images to be stitched:
    for idx in range(len(imgs) - 1):
        im1 = imgs[idx]
        im2 = imgs[idx + 1]
        w  += im1.shape[1]       
  
        # TODO: 1.feature detection & matching
        #refer to https://stackoverflow.com/questions/31690265/matching-features-with-orb-python-opencv
        kp1, des1 = orb.detectAndCompute(im1, None)
        kp2, des2 = orb.detectAndCompute(im2, None)
        matches = bf.knnMatch(des1, des2, k=2)        
        goodu = []
        goodv = []

        for m,n in matches:
            if m.distance < 0.75 * n.distance:
                goodu.append(kp1[m.queryIdx].pt)
                goodv.append(kp2[m.trainIdx].pt)
        goodu = np.array(goodu)
        goodv = np.array(goodv)

        # TODO: 2. apply RANSAC to choose best H
        times = 5000
        threshold = 4
        inlineNmax = 0
        HNmax = np.eye(3)
        for i in range(0, times+1):
            random_u = np.zeros((4,2))
            random_v = np.zeros((4,2)) 
            for j in range(4):
                rint = random.randint(0, len(goodu)-1)
                random_u[j] = goodu[rint]
                random_v[j] = goodv[rint]
            H = solve_homography(random_v, random_u)
            
            onerow = np.ones((1,len(goodu)))
            M = np.concatenate( (np.transpose(goodv), onerow), axis=0)
            W = np.concatenate( (np.transpose(goodu), onerow), axis=0)             
            Mbar = np.dot(H,M)
            Mbar = np.divide(Mbar, Mbar[-1,:])
            
            err  = np.linalg.norm((Mbar-W)[:-1,:], ord=1, axis=0)
            inlineN = sum(err<threshold)
            inline_u = goodu[err<threshold]
            inline_v = goodv[err<threshold]
            
            if inlineN > inlineNmax:
                inlineNmax = inlineN
                HNmax = H

        # TODO: 3. chain the homographies    
        # TODO: 4. apply warping
        last_best_H = last_best_H.dot(HNmax)
        output = warping(im2, dst, last_best_H, 0, im2.shape[0], w, w+im2.shape[1], direction='b') 

    return output


if __name__ == "__main__":

    # ================== Part 4: Panorama ========================
    # TODO: change the number of frames to be stitched
    FRAME_NUM = 2
    imgs = [cv2.imread('../resource/harvard{:d}.jpg'.format(x)) for x in range(1, FRAME_NUM + 1)]
    output4 = panorama(imgs)
    cv2.imwrite('outputHV.png', output4)

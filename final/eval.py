import cv2
import numpy as np
import math
from skimage.measure import compare_ssim
import os
import glob


def psnr(img1, img2):
    mse = np.mean((img1.astype(np.float32) - img2.astype(np.float32)) ** 2)
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    PSNR = 20 * math.log10(PIXEL_MAX / math.sqrt(mse))
    return PSNR

def ssim(img1, img2):
    return compare_ssim(img1.astype(np.float32)/255., img2.astype(np.float32)/255., gaussian_weights=True, sigma=1.5, use_sample_covariance=False, multichannel=True)

if __name__ == '__main__':
    from interp_frame import interp_frame
    """ 0_center_frame """
    sequences = ['0', '1', '2', '3', '4', '5', '6']
    for sq in sequences:
        # read inputs
        I0 = cv2.imread('data/validation/0_center_frame/'+sq+'/input/frame10.png')
        I1 = cv2.imread('data/validation/0_center_frame/'+sq+'/input/frame11.png')
        # interpolate
        It = interp_frame(I0, I1, 0.5)
        if not os.path.exists('output/0_center_frame/'+sq+'/'):
            os.makedirs('output/0_center_frame/'+sq+'/')
        # write output
        cv2.imwrite('output/0_center_frame/'+sq+'/frame10i11.png', It)

        # evaluate
        out = cv2.imread('output/0_center_frame/'+sq+'/frame10i11.png')
        gt = cv2.imread('data/validation/0_center_frame/'+sq+'/GT/frame10i11.png')
        psnr_score = psnr(gt, out)
        ssim_score = ssim(gt, out)
        print(sq, psnr_score, ssim_score)

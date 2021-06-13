import numpy as np
import cv2
import argparse
import os
from JBF import Joint_bilateral_filter


def main():
    parser = argparse.ArgumentParser(description='main function of joint bilateral filter')
    parser.add_argument('--image_path', default='./testdata/2.png', help='path to input image')
    parser.add_argument('--setting_path', default='0', help='path to setting file')
    #parser.add_argument('--setting_path', default='./testdata/1_setting.txt', help='path to setting file')
    args = parser.parse_args()

    img = cv2.imread(args.image_path)
    img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    ### TODO ###
    RGB=np.array(
    [[0.1,0.0,0.9],
    [0.2,0.0,0.8],
    [0.2,0.8,0.0],
    [0.4,0.0,0.6],
    [1.0,0.0,0.0]])
    sigma_s = 1
    sigma_r = 0.05
    
    i = int(args.setting_path)-1
    if i>-1:
    	img_gray = RGB[i,0]*img_rgb[:,:,0] + RGB[i,1]*img_rgb[:,:,1] + RGB[i,2]*img_rgb[:,:,2]

    JBF = Joint_bilateral_filter(sigma_s, sigma_r)
    bf_out = JBF.joint_bilateral_filter(img_rgb, img_rgb).astype(np.uint8)
    jbf_out = JBF.joint_bilateral_filter(img_rgb, img_gray).astype(np.uint8)

    error = np.sum(np.abs(bf_out.astype('int32')-jbf_out.astype('int32')))
    print(error)
    cv2.imshow('origin', img)
    jbf_out = cv2.cvtColor(jbf_out,cv2.COLOR_RGB2BGR)
    cv2.imshow('jbf_out_lowest', jbf_out)
    cv2.imwrite('lowest.png', img_gray)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

import numpy as np
import cv2
import argparse
import os, glob
from eval import evaluate
from computeDisp import computeDisp


def main():
    parser = argparse.ArgumentParser(description='main function of Stereo matching')
    parser.add_argument('--dataset_path', default='./testdata/', help='path to dataset')
    parser.add_argument('--image', choices=['Tsukuba', 'Venus', 'Teddy', 'Cones'], required=True, help='choose processing image')
    args = parser.parse_args()

    config = {'Tsukuba': (15, 16),
              'Venus':   (20, 8),
              'Teddy':   (60, 4),
              'Cones':   (60, 4)}

    img_left = cv2.imread(os.path.join(args.dataset_path, args.image, 'img_left.png'))
    img_right = cv2.imread(os.path.join(args.dataset_path, args.image, 'img_right.png'))
    max_disp, scale_factor = config[args.image]
    
    labels = computeDisp(img_left, img_right, max_disp)
    cv2.imwrite('./%s.png'%args.image, np.uint8(labels * scale_factor))

    gt_path = glob.glob(os.path.join(args.dataset_path, args.image, 'disp_gt.*'))[0]
    if os.path.exists(gt_path):
        img_gt = cv2.imread(gt_path, -1)
        error = evaluate(labels, img_gt, scale_factor)
        print('[Bad Pixel Ratio] %.2f%%' % (error*100))
    

if __name__ == '__main__':
    main()
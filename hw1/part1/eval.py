import numpy as np
import cv2
import argparse
import pickle
from HCD import Harris_corner_detector


def main():
    parser = argparse.ArgumentParser(description='evaluation function of Harris corner detector')
    parser.add_argument('--threshold', default=100., type=float, help='threshold value to determine corner')
    parser.add_argument('--image_path', default='./testdata/ex.png', help='path to input image')
    parser.add_argument('--gt_path', default='./testdata/ex_gt.pkl', help='path to ground truth pickle file')
    args = parser.parse_args()

    img = cv2.imread(args.image_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float64)

    # create HCD class
    HCD = Harris_corner_detector(args.threshold)
    
    response = HCD.detect_harris_corners(img_gray)
    result = HCD.post_processing(response)

    with open(args.gt_path, 'rb') as f:
        gt = pickle.load(f)

    gt_match, out_match = 0, 0
    for gt_coord in gt:
        count = result.count(gt_coord)
        if count >= 1:
            gt_match += 1
            out_match += count
    print('[Error] Result unmatch: %d\n[Error] Ground truth unmatch: %d'%
           (len(gt)-gt_match, len(result)-out_match))


if __name__ == '__main__':
    main()

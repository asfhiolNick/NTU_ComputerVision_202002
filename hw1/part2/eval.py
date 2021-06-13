import numpy as np
import cv2
import argparse
import time
from JBF import Joint_bilateral_filter


def main():
    parser = argparse.ArgumentParser(description='evaluation function of joint bilateral filter')
    parser.add_argument('--sigma_s', default=3, type=int, help='sigma of spatial kernel')
    parser.add_argument('--sigma_r', default=0.1, type=float, help='sigma of range kernel')
    parser.add_argument('--image_path', default='./testdata/ex.png', help='path to input image')
    parser.add_argument('--gt_bf_path', default='./testdata/ex_gt_bf.png', help='path to ground truth bf image')
    parser.add_argument('--gt_jbf_path', default='./testdata/ex_gt_jbf.png', help='path to ground trut jbf image')
    args = parser.parse_args()

    img = cv2.imread(args.image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    guidance = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # create JBF class
    JBF = Joint_bilateral_filter(args.sigma_s, args.sigma_r)
    
    bf_out = JBF.joint_bilateral_filter(img_rgb, img_rgb).astype(np.uint8)
    t0 = time.time()
    jbf_out = JBF.joint_bilateral_filter(img_rgb, guidance).astype(np.uint8)
    print('[Time] %.4f sec'%(time.time()-t0))
    
    bf_gt = cv2.cvtColor(cv2.imread(args.gt_bf_path), cv2.COLOR_BGR2RGB)
    jbf_gt = cv2.cvtColor(cv2.imread(args.gt_jbf_path), cv2.COLOR_BGR2RGB)
    bf_error = np.sum(np.abs(bf_out.astype('int32')-bf_gt.astype('int32')))
    jbf_error = np.sum(np.abs(jbf_out.astype('int32')-jbf_gt.astype('int32')))
    print('[Error] Bilateral: %d\n[Error] Joint bilateral: %d'%
          (bf_error, jbf_error))
    

if __name__ == '__main__':
    main()
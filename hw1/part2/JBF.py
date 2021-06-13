import numpy as np
import cv2


class Joint_bilateral_filter(object):
    def __init__(self, sigma_s, sigma_r):
        self.sigma_r = sigma_r
        self.sigma_s = sigma_s
        self.wndw_size = 6*sigma_s+1
        self.pad_w = 3*sigma_s
    
    def joint_bilateral_filter(self, img, guidance):
        BORDER_TYPE = cv2.BORDER_REFLECT
        padded_img = cv2.copyMakeBorder(img, self.pad_w, self.pad_w, self.pad_w, self.pad_w, BORDER_TYPE)
        padded_guidance = cv2.copyMakeBorder(guidance, self.pad_w, self.pad_w, self.pad_w, self.pad_w, BORDER_TYPE)

        ### TODO ###
        # Step 1: Calculus Gs -- constant matrix
        gs = np.zeros((self.wndw_size, self.wndw_size))
        for i in range(self.wndw_size):
            for j in range(self.wndw_size):
                gs[i,j] = np.exp( np.divide(np.square(i-self.pad_w)+np.square(j-self.pad_w),-2*self.sigma_s*self.sigma_s) )

        # Step 2: Normalize guidance(gray)
        padded_guidance = padded_guidance.astype('float64')
        padded_guidance /= 255

        # Step 3: Calculus Gr with guidance(gray), G:=Gr*Gs, JB-filter I->I'
        padded_img = padded_img.astype('float64')
        output = np.zeros(img.shape)

        for i in range(self.pad_w, padded_guidance.shape[0]-self.pad_w):
            for j in range(self.pad_w, padded_guidance.shape[1]-self.pad_w):
                #Step 3-1: Calculus Gr with guidance(gray)
                Tp = padded_guidance[i,j]
                Tq = padded_guidance[i-self.pad_w:i+self.pad_w+1, j-self.pad_w:j+self.pad_w+1]
                pw = np.divide(np.square(Tp-Tq), -2*self.sigma_r*self.sigma_r)
                if len(pw.shape)==3:
                    pw = pw.sum(axis=2)  
                Gr=np.exp(pw)

                #Step 3-2: Calculus G:=Gr*Gs
                G =np.multiply(gs, Gr)
                W =G.sum(axis=1).sum(axis=0)

                #Step 3-3: JB-filter I->I'  
                Iq=padded_img[i-self.pad_w:i+self.pad_w+1, j-self.pad_w:j+self.pad_w+1]        
                for k in range(img.shape[2]):
                    output[i-self.pad_w, j-self.pad_w, k] = np.multiply(G,Iq[:,:,k]).sum(axis=1).sum(axis=0)/W
        output.astype(np.uint8)

        return np.clip(output, 0, 255).astype(np.uint8)

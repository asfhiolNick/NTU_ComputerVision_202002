import numpy as np
import cv2.ximgproc as xip
import cv2

def dist(M1, M2):
    #L2, with half = 0
    #return np.sum( np.square(M1 - M2) )
 
    #L1, with half = 0
    return np.sum(np.abs( M1 - M2 ))

    #Census, with half = 1  
    '''
    ans = 0
    for c in range(M1.shape[2]):
        for i in range(3):
            for j in range(3):
                ans += int( (M1[i, j, c]<M1[1,1,c])^(M2[i,j, c]<M2[1,1,c]) )
    return ans
    '''

    

def computeDisp(Il, Ir, max_disp):
    h, w, ch = Il.shape
    labels = np.zeros((h, w), dtype=np.float32)
    Il = Il.astype(np.float32)
    Ir = Ir.astype(np.float32)

    # >>> Cost Computation
    # TODO: Compute matching cost
    # [Tips] Census cost = Local binary pattern -> Hamming distance
    # [Tips] Set costs of out-of-bound pixels = cost of closest valid pixel  
    # [Tips] Compute cost both Il to Ir and Ir to Il for later left-right consistency

    # >>> Cost Aggregation
    # TODO: Refine the cost according to nearby costs
    # [Tips] Joint bilateral filter (for the cost of each disparty) 
    cost_Il2Ir = np.zeros((max_disp+1, h, w), dtype=np.float32)
    cost_Ir2Il = np.zeros((max_disp+1, h, w), dtype=np.float32)

    for s in range(max_disp+1):
        for x in range(w): 
            xs_lft = max(x-s, 0)
            xs_rig = min(x+s, w-1)
            for y in range(h):
                cost_Il2Ir[s, y, x] = dist(Il[y, x], Ir[y, xs_lft])
                cost_Ir2Il[s, y, x] = dist(Ir[y, x], Il[y, xs_rig])
        cost_Il2Ir[s,] = xip.jointBilateralFilter(Il, cost_Il2Ir[s,], 30, 5, 5)
        cost_Ir2Il[s,] = xip.jointBilateralFilter(Ir, cost_Ir2Il[s,], 30, 5, 5)  


    # >>> Disparity Optimization
    # TODO: Determine disparity based on estimated cost.
    # [Tips] Winner-take-all
    winner_dispL = np.argmin(cost_Il2Ir, axis=0)
    winner_dispR = np.argmin(cost_Ir2Il, axis=0)

    # >>> Disparity Refinement
    # TODO: Do whatever to enhance the disparity map
    # [Tips] Left-right consistency check -> Hole filling -> Weighted median filtering
    for y in range(h):
        for x in range(w):
            if x-winner_dispL[y,x]>=0 and winner_dispL[y,x] == winner_dispR[y,x-winner_dispL[y,x]]:
                continue
            else:
                winner_dispL[y,x]=-1

    for y in range(h):
        for x in range(w):
            if winner_dispL[y,x] == -1:
                l = 0
                r = 0
                while x-l>=0 and winner_dispL[y,x-l] == -1:
                    l+=1
                if x-l < 0:
                    FL = max_disp 
                else:
                    FL = winner_dispL[y,x-l]

                while x+r<=w-1 and winner_dispL[y,x+r] == -1:
                    r+=1
                if x+r > w-1:
                    FR = max_disp
                else:
                    FR = winner_dispL[y, x+r]
                winner_dispL[y,x] = min(FL, FR)
   
    labels = xip.weightedMedianFilter(Il.astype(np.uint8), winner_dispL.astype(np.uint8), 18, 1)
    return labels.astype(np.uint8)
    

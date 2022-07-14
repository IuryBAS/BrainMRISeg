import numpy as np
from skimage.segmentation import chan_vese
import utils


def apply_chan_vese(mri_img, point_markers, mu, lambda1, lambda2):
    mask = np.zeros(mri_img.shape)

    cv = chan_vese(mri_img, mu, lambda1, lambda2, tol=1e-3,
                   max_num_iter=150, dt=0.5, init_level_set="checkerboard",
                   extended_output=True)

    mri_img = utils.normalize_img(mri_img).astype(np.uint8)

    mask[np.where(cv[0] == False)] = 1
    mask[np.where(cv[0] == True)] = 0

    mask = mask.astype(np.uint8)

    y, x = point_markers

    Xi = np.zeros(mri_img.shape)
    w = np.matrix('0 1 0; 1 1 1; 0 1 0').astype(np.uint8)
    Xi[x, y] = 1

    flag = True
    while flag:
        X_i = utils.dilation(Xi, w)
        X_i = np.bitwise_and(X_i == 1, mask == 1).astype(np.uint8)
        if np.sum(X_i - Xi) == 0:
            flag = False
        Xi = X_i

    mri_marked = np.copy(mri_img)
    mri_marked[np.where(Xi == 1)] = 255

    return mri_marked

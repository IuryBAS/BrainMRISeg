import numpy as np
from skimage.segmentation import chan_vese


def dilation(f, w):
    m, n = w.shape

    mf, nf = f.shape

    a = int((m - 1) / 2)
    b = int((n - 1) / 2)

    r = np.copy(f)

    for xf in range(a, mf - a):
        for yf in range(b, nf - b):
            sub_f = f[xf - a: xf + a + 1, yf - b: yf + b + 1]
            r[xf, yf] = sub_f.max()

    return r.astype(np.uint8)


def apply_chan_vese(mri_img, point_markers, mu, lambda1, lambda2):
    '''
    Function to apply chan-vese segmentation on input image.

    Params:
        mri_img: The input image to be processed;
        mu, lambda1, lambda: Variables of metod;

    cha_vesse returns: An array cv with length 4, where:
        cv[0]: Original image;
        cv[1]: Segmentation after iterations;
        cv[2]: Final level set;
        cv[3]: Evolution of energy over iterations;

    Returns:
        An segmentated image with mask.


    '''
    mask = np.zeros(mri_img.shape)

    cv = chan_vese(mri_img, mu, lambda1, lambda2, tol=1e-3,
                   max_num_iter=150, dt=0.5, init_level_set="checkerboard",
                   extended_output=True)

    mask[np.where(cv[0] == False)] = 1
    mask[np.where(cv[0] == True)] = 0

    mask = mask.astype(np.uint8)

    # Point to do morphology, taking the connected part of segmentation
    y, x = point_markers

    Xi = np.zeros(mri_img.shape)
    w = np.matrix('0 1 0; 1 1 1; 0 1 0').astype(np.uint8)
    Xi[x, y] = 1

    flag = True
    while flag:
        X_i = dilation(Xi, w)
        X_i = np.bitwise_and(X_i == 1, mask == 1).astype(np.uint8)
        if np.sum(X_i - Xi) == 0:
            flag = False
        Xi = X_i

    mri_marked = np.copy(mri_img)
    mri_marked[np.where(Xi == 1)] = 255

    return mri_marked

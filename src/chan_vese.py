import numpy as np
from skimage.segmentation import chan_vese


def normalize_img(image, imax=8, dtype=np.uint8):
    '''
    Normalize an image between its maximum and minimum values, and with the
    specifield caracteristics

    Params:
        image: An image to be normalized
        imax: The value of bits to represent the pixel values
        dtype: The desired dtype of the image

    Returns:
        A normalized image
    '''
    img_max = np.max(image)
    img_min = np.min(image)

    # Prevents division by 0 when the img_max and img_min have the same value
    if img_max == img_min:
        img_sub_norm = (image-img_min) / ((img_max - img_min) + 1e-12)

    else:
        img_sub_norm = (image-img_min) / (img_max - img_min)
    # Normalize image accordinly with the maximum bits representation
    # passed as parameter
    img_sub_norm = (img_sub_norm * ((2**imax) - 1)).astype(dtype)
    return img_sub_norm


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

    return Xi























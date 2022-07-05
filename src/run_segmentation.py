import watershed
import numpy as np
import utils
import matplotlib.pyplot as plt
import math
import args_test_watershed
import chan_vese

def plot_mosaic(slices_array, slice_range):

    start_slice, end_slice = slice_range
    n_cols = 4
    n_rows = math.ceil((end_slice - start_slice) / n_cols)
    fig, axs = plt.subplots(nrows=n_rows, ncols=n_cols)

    for i, slice_sub in enumerate(slices_array):
        ax = plt.subplot(n_rows, n_cols, i+1)
        plt.imshow(slice_sub, cmap='gray')
    


def get_batch_data(df, subject_id, slices_range, perspective, masks=False):
    start_slice, end_slice = slices_range
    slices_array = []
    masks_array = []
    for n_slice in range(start_slice, end_slice):
        slice_n = utils.get_image(df, subject_id, n_slice, perspective, masks)
        slices_array.append(np.flip(slice_n))
    
    return slices_array


def apply_batch_watershed(df, subject_id, slices_range, perspective, norm_thres,
                          morph_args, x, y, outer_x, outer_y):

    slices_array = get_batch_data(df, subject_id, slices_range, perspective)
    masks_array = get_batch_data(df, subject_id, slices_range, perspective, True)
    mask = [[x, y], [outer_x, outer_y]]
    seg_masks_array = []
    for slice in slices_array:
        
        mri_norm = utils.normalize_img(slice)
        mri_thresholded = mri_norm.copy()

        if norm_thres:
           mri_thresholded[mri_thresholded >= norm_thres] = 255

        mri_denoised = watershed.apply_morphology(mri_thresholded, **morph_args)
        img_seg = watershed.apply_watershed(mri_denoised, mask)
        img_seg[img_seg != 2] = 0
        seg_masks_array.append(img_seg)

        

    plot_mosaic(seg_masks_array, slices_range)
    plot_mosaic(masks_array, slices_range)
    plt.show()


def apply_batch_chan_vese(df, subject_id, slices_range, perspective, mu, lambda1, lambda2, x, y):
    slices_array = get_batch_data(df, subject_id, slices_range, perspective)
    seg_masks_array = []
    for slice in slices_array:
        img_seg = chan_vese.apply_chan_vese(slice, (x, y), mu, lambda1, lambda2)
        seg_masks_array.append(img_seg)

    plot_mosaic(seg_masks_array, slices_range)
    plt.show()


if __name__ == '__main__':

    df = utils.build_dataframe('../Episurg', 'subjects.csv')
    
    CASES = args_test_watershed.TESTE_CASES

    for case_test in CASES:
        sub_id = case_test['subject_id']
        slices_range = case_test['slice_range']
        perspective = case_test['perspective']
        norm_thres = case_test['norm_thres']
        morphy = case_test['apply_morphy']
        x = case_test['x']
        y = case_test['y']
        outer_x = case_test['outer_mark_x']
        outer_y = case_test['outer_mark_y']
        mu = case_test['mu']
        lambda1 = case_test['lambda1']
        lambda2 = case_test['lambda2']
        apply_batch_chan_vese(df, sub_id, slices_range, perspective, mu, lambda1, lambda2, x, y)
        apply_batch_watershed(df, sub_id, slices_range, perspective, norm_thres,
                              morphy, x, y, outer_x, outer_y)



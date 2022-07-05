import watershed
import numpy as np
import utils
import matplotlib.pyplot as plt
import math
import args_test_watershed
import chan_vese


def plot_mosaic(slices_array, slice_range, title):

    start_slice, end_slice = slice_range
    n_cols = 4
    n_rows = math.ceil((end_slice - start_slice) / n_cols)
    fig, axs = plt.subplots(nrows=n_rows, ncols=n_cols)

    for i, slice_sub in enumerate(slices_array):
        ax = plt.subplot(n_rows, n_cols, i+1)
        ax.title.set_text(title)
        plt.imshow(slice_sub, cmap='gray')


def get_batch_data(df, subject_id, slices_range, perspective, masks=False):
    start_slice, end_slice = slices_range
    slices_array = []
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
    dice_scores = []

    for slice, gt_mask in zip(slices_array, masks_array):
        mri_norm = utils.normalize_img(slice)
        mri_thresholded = mri_norm.copy()

        if norm_thres:
            mri_thresholded[mri_thresholded >= norm_thres] = 255

        mri_denoised = watershed.apply_morphology(mri_thresholded, **morph_args)
        img_seg = watershed.apply_watershed(mri_denoised, mask)
        img_seg[img_seg != 2] = 0
        img_seg[img_seg == 2] = 1

        dice_score = dice_score_similarity(img_seg, gt_mask, 1)
        dice_scores.append(dice_score)
        seg_masks_array.append(img_seg)

    plot_mosaic(seg_masks_array, slices_range, 'Seg Watershed')
    plot_mosaic(masks_array, slices_range, 'Seg GT')

    return np.asarray(dice_scores)


def apply_batch_chan_vese(df, subject_id, slices_range, perspective, mu, 
                          lambda1, lambda2, x, y):

    slices_array = get_batch_data(df, subject_id, slices_range, perspective)
    masks_array = get_batch_data(df, subject_id, slices_range, perspective, True)
    seg_masks_array = []
    dice_scores = []

    for slice, gt_mask in zip(slices_array, masks_array):
        img_seg = chan_vese.apply_chan_vese(slice, (x, y), mu, lambda1, lambda2)
        dice_score = dice_score_similarity(img_seg, gt_mask)
        dice_scores.append(dice_score)
        seg_masks_array.append(img_seg)

    plot_mosaic(seg_masks_array, slices_range, 'Seg Chan Vese')

    return np.asarray(dice_scores)


def dice_score_similarity(prev_seg, bg_mask, value_mask=1):

    dice_score = np.sum(prev_seg[bg_mask == value_mask]) * 2.0
    dice_score /= (np.sum(prev_seg) + np.sum(bg_mask))
    return dice_score


if __name__ == '__main__':

    df = utils.build_dataframe('../Episurg', 'subjects.csv')

    CASES = args_test_watershed.TESTE_CASES
    dices_scores_watershed = []
    dices_scores_chan_vese = []

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
        dices_chan = apply_batch_chan_vese(df, sub_id, slices_range, perspective,
                                           mu, lambda1, lambda2, x, y)
        dices_water = apply_batch_watershed(df, sub_id, slices_range,
                                            perspective, norm_thres, morphy, x,
                                            y, outer_x, outer_y)

        dices_scores_chan_vese.append(dices_chan)
        dices_scores_watershed.append(dices_water)
        #plt.show()

    i = 1
    for score_chan, score_water in zip(dices_scores_chan_vese, dices_scores_watershed):
        print('Mean water for case {}: {}'.format(i, np.mean(score_water)))
        print('Mean chan for case {}: {}'.format(i, np.mean(score_chan)))
        i += 1

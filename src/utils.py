import numpy as np
import pandas as pd
import nibabel as nib
import matplotlib.pyplot as plt
from glob import glob


def _get_nii_paths(dataset_path, id_sub):
    '''
    Function to get the path os the nii files given a subject id.
    Params:
        dataset_path: The path to the dataset files
        id_sub: Subject's id

    Return:
        files: List of nii files of the subject
    '''
    search_str = '{}/subjects/{}/*/*nii.gz'.format(dataset_path, id_sub)
    files = glob(search_str, recursive=True)
    return files


def build_dataframe(dataset_path, csv_filename, filter_with_mask=True):
    '''
    Build the dataframe given the dataset. For the episurg, the subjects
    are filtered to only include that with at least one segmentation mask.
    The final dataset contains informations about the subject and the
    dir of the nii files

    Params:
        dataset_path: Path to the dataset folder
        csv_filename: Filename of the csv describing the dataset and subjects
        filter_with_mask: Flag to filter the subjects to be included to only
        allow cases where at least one mask is present

    Returns:
        df_subjects: A dataframe of the subjects with its nii files paths
    '''
    df_subjects = pd.read_csv('{}/{}'.format(dataset_path, csv_filename))
    # Filter only the subjects with at least one segmentation mask
    if filter_with_mask:
        df_subjects = df_subjects[df_subjects['Rater1']
                                  | df_subjects['Rater2']
                                  | df_subjects['Rater3']
                                  ]
    for sub in df_subjects.iterrows():
        sub_id = sub[1]['Subject']
        nii_paths = _get_nii_paths(dataset_path, sub_id)
        seg1, seg2, seg3 = '', '', ''
        t1 = ''
        for nii_f in nii_paths:
            nii_split = nii_f.split('_')
            nii_type = nii_split[-1]
            if 'seg-1' in nii_type:
                seg1 = nii_f
            if 'seg-2' in nii_type:
                seg2 = nii_f
            if 'seg-3' in nii_type:
                seg3 = nii_f
            if 't1' in nii_type and 'postop' in nii_type:
                t1 = nii_f
        dict_nii = {'t1': t1, 'seg1': seg1, 'seg2': seg2, 'seg3': seg3}
        df_subjects.loc[sub[0], ['t1', 'seg1', 'seg2', 'seg3']] = dict_nii
    return df_subjects


def get_image(df, subject_id, slice_n, perspective, mask=False):
    '''
    Function to return an slice of an specific subject given a desired
    perspective as a regular bi-dimensional gray scale image or binary segment
    mask

    Params:
        df: A dataframe containing the subjects ids and the paths for the
        nii files of the T1 volumes and segmentation masks
        subject_id: The id of the target subject
        slice_n: The number of the desired volume slice
        perspective: The key for the desired perspective of the volume,
        which can be "a" for axial, "c" for coronal and "s" for saggital
        mask: When return the T1 volume or the segmentation mask

    Returns:
        A regular bi-dimensional gray scale image or binary mask of the desired
        volume slice in the given perspective for the given subject

    '''
    subject = 'sub-{}'.format(subject_id)
    # If not a mask, get the mri image itself. If mask, return the human made
    # mask for the slice subject. In this project, we consider only the mask 1
    # for simplicity
    if not mask:
        image_path = df.loc[df['Subject'] == subject].t1.values[0]
    else:
        image_path = df.loc[df['Subject'] == subject].seg1.values[0]
    img_mri = nib.load(image_path).get_fdata()
    # Get the image in the desired perspective
    if perspective == 'a':
        img_slice = img_mri[:, slice_n, :]
    elif perspective == 's':
        img_slice = img_mri[slice_n, :, :]
    elif perspective == 'c':
        img_slice = img_mri[:, :, slice_n]
    
    # Transpose de image to put it in the correct orientation
    img = np.transpose(img_slice)
    return img


def show_nii(img):
    plt.imshow(img, cmap='gray')
    plt.show()


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

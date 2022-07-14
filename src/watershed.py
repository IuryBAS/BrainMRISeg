import numpy as np
from skimage.segmentation import watershed


def apply_morphology(input_image, **kwargs):
    '''
    Function to apply the morphology procedures in an input image. Several
    methods can be applied in batch, being executed in sequence

    Params:
        input_image: The input image to be processed
        kwargs: An title of the procedure, the method function and a structural
        element
        Ex:
            apply_morphology(image, denoise_1={'method':denoise_func,
                                               'se':structual_element
                                               },
                                    threshold_1={'method':threshold_func,
                                                 'se': structual_element
                                                }
                            )
        Returns: A processed result image by the methods performed in sequence

    '''
    img = input_image

    # Apply each preprocessing procedure in sequence, given in as the kwargs 
    # of the function
    for kw in kwargs:
        apply_morph = kwargs[kw]
        # Get the method procedure to be perfomed
        method = apply_morph['method']
        # Get the structual element
        struct_element = apply_morph['se']
        img = method(img, struct_element)

    return img


def apply_watershed(input_image, point_markers, same_markers=False):
    '''
    Function to perform the watershed segmentation given an input image and
    a list of seeds. The seeds could be labeled as an unique label or different
    labels

    Params:
        input_image: The input image to be segmented
        point_markers: A list of points [x, y] representing pixels to be used
        as seeds
        same_markers: Flag to indicate when use the same label to all the seeds
        or not

    Returns:
        An segmentated mask of the image
    '''
    markers = np.zeros_like(input_image)
    # Set a seed in the background area of the MRI image, outside of the brain
    markers[0][0] = 1

    # Set labels for each ponint marker. If multiple markers represent the same
    # segment, label them with the same value. 
    for label, coord_p in enumerate(point_markers):
        y, x = coord_p
        if same_markers:
            markers[x, y] = 2
        else:
            markers[x, y] = label + 2

    segmented_image = watershed(input_image, markers)
    return segmented_image


'''
def onclick(event):
    X_coordinate = int(event.xdata)
    Y_coordinate = int(event.ydata)
    coords.append([X_coordinate, Y_coordinate])
'''

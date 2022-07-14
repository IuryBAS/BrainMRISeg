from skimage.filters import rank
from skimage.morphology import disk, square, diamond, rectangle
from skimage.morphology import erosion, dilation, opening, closing

CASE_1 = {'subject_id': '0018',
          'slice_range': (173, 182),
          'perspective': 'a',
          'norm_thres': None,
          'apply_morphy': {'denoise_1': {'method': rank.median, 'se': disk(2)},
                           'gradient_1': {'method': rank.gradient, 'se': disk(1)}
                           },
          'x': 116,
          'y': 85,
          'outer_mark_x': 109,
          'outer_mark_y': 99,
          'mu': 0.15,
          'lambda1': 1,
          'lambda2': 1
          }

CASE_2 = {'subject_id': '0317',
          'slice_range': (173, 182),
          'perspective': 'a',
          'norm_thres': 19,
          'apply_morphy': {'denoise_1': {'method': rank.mean, 'se': disk(1)},
                           'closing_1': {'method': closing, 'se': rectangle(5,1)},
                           'closing_2': {'method': closing, 'se': disk(1)},
                           'gradient_1': {'method': rank.gradient, 'se': disk(1)}
                           },
          'x': 155,
          'y': 103,
          'outer_mark_x': 109,
          'outer_mark_y': 99,
          'mu': 0.1,
          'lambda1': 1,
          'lambda2': 1
          }

CASE_3 = {'subject_id': '0023',
          'slice_range': (165, 172),
          'perspective': 'a',
          'norm_thres': 20,
          'apply_morphy': {'denoise_1': {'method': rank.mean, 'se': disk(1)},
                           'gradient_1': {'method': rank.gradient, 'se': disk(1)},
                           'closing_1': {'method': closing, 'se': square(1)},
                           },
          'x': 143,
          'y': 143,
          'outer_mark_x': 109,
          'outer_mark_y': 99,
          'mu': 0.08,
          'lambda1': 1,
          'lambda2': 1
          }

CASE_4 = {'subject_id': '0035',
          'slice_range': (114, 120),
          'perspective': 'a',
          'norm_thres': 50,
          'apply_morphy': {'denoise_1': {'method': rank.median, 'se': disk(2)},
                           'closing_1': {'method': closing, 'se': disk(7)},
                           'gradient_1': {'method': rank.gradient, 'se': disk(1)},
                           },
          'x': 166,
          'y': 100,
          'outer_mark_x': 109,
          'outer_mark_y': 99,
          'mu': 0.1,
          'lambda1': 1,
          'lambda2': 1.3
          }


TESTE_CASES = [CASE_1, CASE_2, CASE_3, CASE_4]

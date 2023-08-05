import itertools as it
import numpy as np


def apply_2d_trafo(trafo_2d, array_5d, **kwargs):
    array_out_5d = np.zeros_like(array_5d)
    n_t, n_z, n_c, n_x, n_y = np.shape(array_out_5d)

    for t, z, c in it.product(range(n_t), range(n_z), range(n_c)):
        array_out_5d[t, z, c, :, :] = trafo_2d(array_5d[t, z, c, :, :], kwargs)

    return array_out_5d


def apply_3d_trafo_zstack(trafo_3d, array_5d, **kwargs):
    array_out_5d = np.zeros_like(array_5d)
    n_t, n_z, n_c, n_x, n_y = np.shape(array_out_5d)

    for t, c in it.product(range(n_t), range(n_c)):
        array_out_5d[t, :, c, :, :] = trafo_3d(array_5d[t, :, c, :, :], kwargs)

    return array_out_5d


def apply_3d_trafo_rgb(trafo_3d, array_5d, **kwargs):
    array_out_5d = np.zeros_like(array_5d)
    n_t, n_z, n_c, n_x, n_y = np.shape(array_out_5d)

    for t, z in it.product(range(n_t), range(n_z)):
        array_out_5d[t, z, :, :, :] = trafo_3d(array_5d[t, z, :, :, :], kwargs)

    return array_out_5d

import numpy as np
from PIL import ImageSequence


def fn(img, percentile=2.5):
    '''

    Parameters
    ----------
    img : PIL.Image
        An image sequence, such as a TIFF stack.
    percentile : float, optional
        Default is 2.5.

    Returns
    -------
    numpy.ndarray
        yeah that's a thing
    '''
    background = np.empty((img.n_frames))
    for index, frame in zip(range(img.n_frames), ImageSequence.Iterator(img)):
        background[index] = np.percentile(frame, percentile)
    return background

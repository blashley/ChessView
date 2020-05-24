import numpy as np
from PIL import Image
from scipy.signal import convolve, find_peaks

""" This is the accompanying .py file for comp_vision.ipynb. See the notebook for a walkthrough of this function. """

def split_image(pil_img):
    pil_img = pil_img.convert('L')
    img = np.array(pil_img)
    height, width = img.shape

    ker_x = np.array(np.mat('-1 0 1; -1 0 1; -1 0 1'))
    grad_x = convolve(img, ker_x)
    ker_y = np.array(np.mat('-1 -1 -1; 0 0 0; 1 1 1'))
    grad_y = convolve(img, ker_y)

    x_pos = np.clip(grad_x, 0, 255)
    x_neg = np.clip(grad_x, -255, 0)
    y_pos = np.clip(grad_y, 0, 255)
    y_neg = np.clip(grad_y, -255, 0)

    row_sums = np.sum(y_pos/height, axis=1) * np.sum(-y_neg/height, axis=1)
    row_sums[np.where(row_sums<np.max(row_sums)/2)] = 0
    col_sums = np.sum(x_pos/width, axis=0) * np.sum(-x_neg/width, axis=0)
    col_sums[np.where(col_sums<np.max(col_sums)/2)] = 0

    cols = list(find_peaks(col_sums, distance=10)[0])
    rows = list(find_peaks(row_sums, distance=10)[0])

    def near_arith_prog(arr):
        diffs = [arr[i] - arr[i-1] for i in range(1,len(arr))]
        return max(diffs) - min(diffs) < 5

    def get_lines(arr):
        if len(arr) < 7:
            return None
        elif len(arr) == 7:
            if near_arith_prog(arr):
                return arr
            else:
                return None
        elif len(arr) == 8:
            if near_arith_prog(arr[:7]):
                return arr[:7]
            elif near_arith_prog(arr[1:]):
                return arr[1:]
        elif len(arr) == 9:
            if near_arith_prog(arr[1:8]):
                return arr[1:8]
        return None

    cols = get_lines(cols)
    rows = get_lines(rows)
    
    if not cols or not rows:
        return None

    sq_height = rows[1] - rows[0]
    sq_width = cols[1] - cols[0]  # Allow for rectangles
    # Add left and right external edges
    cols.append(min(cols[6] + sq_width, width))
    cols.insert(0, max(cols[0] - sq_width, 0))
    # Add top and bottom external edges
    rows.append(min(rows[6] + sq_height, height))
    rows.insert(0, max(rows[0] - sq_height, 0))

    squares = []
    # Traverse board in order described by FEN
    for j in range(len(rows)-1):
        for i in range(len(cols)-1):
            area = (cols[i], rows[j], cols[i+1], rows[j+1])
            squares.append(pil_img.crop(area).resize((32,32), resample=Image.LANCZOS))
    return squares

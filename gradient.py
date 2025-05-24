from PIL import Image, ImageTk
import numpy as np
import tkinter as tk
import sys

bayer = np.array([
    [ 0,  8,  2, 10],
    [12,  4, 14,  6],
    [ 3, 11,  1,  9],
    [15,  7, 13,  5]
]) / 16.0

big_bayer = np.array([
    [ 0, 32,  8, 40,  2, 34, 10, 42],
    [48, 16, 56, 24, 50, 18, 58, 26],
    [12, 44,  4, 35, 14, 46,  6, 38],
    [60, 28, 52, 20, 62, 30, 54, 22],
    [ 3, 35, 11, 43,  1, 33,  9, 41],
    [51, 19, 59, 27, 49, 17, 57, 25],
    [15, 47,  7, 39, 13, 45,  5, 37],
    [63, 31, 55, 23, 61, 29, 53, 21]
]) / 64.

def generate_bayer_matrix(n):
    if n == 2:
        return np.array([[0,2],[3,1]])
    # else:
    smaller_matrix = generate_bayer_matrix(n // 2)
    return np.block([
        [4 * smaller_matrix, 4 * smaller_matrix + 2],
        [4 * smaller_matrix + 3, 4 * smaller_matrix + 1]
    ])

# 生成 16x16 Bayer 矩陣
bayer_16x16 = generate_bayer_matrix(16)
print(bayer_16x16)
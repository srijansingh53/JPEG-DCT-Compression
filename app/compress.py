import cv2
import numpy as np
import math
import pathlib
from dct_idct import dct_2d, idct_2d

def selectQMatrix(qName):
    Q10 = np.array([[80,60,50,80,120,200,255,255],
                [55,60,70,95,130,255,255,255],
                [70,65,80,120,200,255,255,255],
                [70,85,110,145,255,255,255,255],
                [90,110,185,255,255,255,255,255],
                [120,175,255,255,255,255,255,255],
                [245,255,255,255,255,255,255,255],
                [255,255,255,255,255,255,255,255]])

    Q50 = np.array([[16,11,10,16,24,40,51,61],
                [12,12,14,19,26,58,60,55],
                [14,13,16,24,40,57,69,56],
                [14,17,22,29,51,87,80,62],
                [18,22,37,56,68,109,103,77],
                [24,35,55,64,81,104,113,92],
                [49,64,78,87,103,121,120,101],
                [72,92,95,98,112,100,130,99]])

    Q90 = np.array([[3,2,2,3,5,8,10,12],
                    [2,2,3,4,5,12,12,11],
                    [3,3,3,5,8,11,14,11],
                    [3,3,4,6,10,17,16,12],
                    [4,4,7,11,14,22,21,15],
                    [5,7,11,13,16,12,23,18],
                    [10,13,16,17,21,24,24,21],
                    [14,18,19,20,22,20,20,20]])
    if qName == 1:
        return Q10
    elif qName == 2:
        return Q50
    elif qName == 3:
        return Q90
    else:
        return np.ones((8,8))


def Compress(filepath,rate):
    # defining block size
    block_size = 8

    # Quantization Matrix
    QUANTIZATION_MAT = selectQMatrix(rate)

    # reading image in grayscale style
    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)



    # get size of the image
    [h , w] = img.shape



    # No of blocks needed : Calculation

    height = h
    width = w
    h = np.float32(h)
    w = np.float32(w)

    nbh = math.ceil(h/block_size)
    nbh = np.int32(nbh)

    nbw = math.ceil(w/block_size)
    nbw = np.int32(nbw)


    # Pad the image, because sometime image size is not dividable to block size
    # get the size of padded image by multiplying block size by number of blocks in height/width

    # height of padded image
    H =  block_size * nbh

    # width of padded image
    W =  block_size * nbw

    # create a numpy zero matrix with size of H,W
    padded_img = np.zeros((H,W))

    # copy the values of img into padded_img[0:h,0:w]
    padded_img[0:height,0:width] = img[0:height,0:width]

    cv2.imwrite('static/compressed/uncompressed.bmp', np.uint8(padded_img))



    # start encoding:
    # divide image into block size by block size (here: 8-by-8) blocks
    # To each block apply 2D discrete cosine transform
    for i in range(nbh):

            # Compute start and end row index of the block
            row_ind_1 = i*block_size
            row_ind_2 = row_ind_1+block_size

            for j in range(nbw):

                # Compute start & end column index of the block
                col_ind_1 = j*block_size
                col_ind_2 = col_ind_1+block_size

                block = padded_img[ row_ind_1 : row_ind_2 , col_ind_1 : col_ind_2 ]
                # print(type(block))
                # apply 2D discrete cosine transform to the selected block
                # DCT = dct_2d(block) # scratch dct2d is taking time 
                DCT = cv2.dct(block)

                DCT_normalized = np.divide(DCT,QUANTIZATION_MAT).astype(int)

                # copy reshaped matrix into padded_img on current block corresponding indices
                padded_img[row_ind_1 : row_ind_2 , col_ind_1 : col_ind_2] = DCT_normalized

    # cv2.imshow('encoded image', np.uint8(padded_img))

    cv2.imwrite('static/compressed/quantized.bmp',padded_img)

    i = 0
    j = 0
    # initialisation of compressed image
    comp_img = np.zeros((H,W))

    while i < H:
        j = 0
        while j < W:
            block = padded_img[i:i+8,j:j+8]
            # print(block)
            de_quantized = np.multiply(block,QUANTIZATION_MAT)
            # inverse = idct_2d(np.float64(de_quantized)) # # scratch dct2d is taking time 
            inverse = cv2.idct(np.float64(de_quantized))
            # print(inverse)
            comp_img[i:i+8,j:j+8] = inverse
            j = j + 8
        i = i + 8

    comp_img[padded_img > 255] = 255
    comp_img[padded_img < 0] = 0
    # print(np.amin(padded_img))
    # compressed image is written into compressed_image.mp file
    cv2.imwrite("static/compressed/compressed_image.bmp",np.uint8(comp_img))
    output_path = 'compressed_image.bmp'
    # print(output_path)
    return output_path

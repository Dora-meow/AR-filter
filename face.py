from PIL import Image
import numpy as np
import os
def convolve(image, kernel, stride=1, padding=0):
    img_h, img_w = image.shape
    kernel_h, kernel_w = kernel.shape
    padded_image = np.pad(image, ((padding, padding), (padding, padding)), mode='constant', constant_values=0)
    padded_h, padded_w = padded_image.shape
    out_h = (padded_h - kernel_h) // stride + 1
    out_w = (padded_w - kernel_w) // stride + 1
    output = np.zeros((out_h, out_w))
    for y in range(0, out_h):
        for x in range(0, out_w):
            region = padded_image[y * stride : y * stride + kernel_h, x * stride : x * stride + kernel_w]
            output[y, x] = np.sum(region * kernel)

    return output
def detect_face(image_array):
    image_array+=1
    kernal = np.array([
                [ -6, -5, -3, -2, -1,  0,  0,  0,  0,  1,  0,  0,  0,  0, -1, -2, -3, -5, -6],
                [ -5, -3, -2, -1,  0,  0,  0,  0,  1,  1,  1,  0,  0,  0,  0, -1, -2, -3, -5],
                [ -3, -2, -1,  0,  0,  0,  0,  1,  2,  1,  3,  1,  0,  0,  0,  0, -1, -2, -3],
                [ -2, -1,  0,  0,  0,  0,  1,  2,  1,  2,  1,  2,  1,  0,  0,  0,  0, -1, -2],
                [ -2, -1,  0,  0,  0,  1,  2,  1,  0,  1,  0,  1,  2,  1,  0,  0,  0, -1, -2],
                [ -2, -1,  0,  0,  1,  2,  1,  0,  0,  0,  0,  0,  1,  2,  1,  0,  0, -1, -2],
                [ -1,  0,  0,  1,  2,  1,  0,  0,  0,  0,  0,  0,  0,  1,  2,  1,  0,  0, -1],
                [  0,  0,  1,  2,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  2,  1,  0,  0],
                [  1,  1,  2,  1,  0,  0,  1,  0,  0,  0,  0,  0,  1,  0,  0,  1,  2,  1,  1],
                [  1,  2,  1,  0,  1,  1,  2,  1,  1,  0,  1,  1,  3,  1,  1,  0,  1,  2,  1],
                [  1,  2,  1,  0,  1,  3,  4,  3,  1,  1,  1,  3,  4,  3,  1,  0,  1,  2,  1],
                [  1,  2,  1,  0,  1,  1,  1,  1,  1,  0,  1,  1,  2,  1,  1,  0,  1,  2,  1],
                [  0,  1,  2,  1,  0,  0,  0,  0,  1,  1,  1,  0,  0,  0,  0,  1,  2,  1,  0],
                [  0,  0,  1,  2,  1,  0,  0,  0,  1,  2,  1,  0,  0,  0,  1,  2,  1,  0,  0],
                [  0,  0,  0,  1,  2,  1,  0,  1,  2,  3,  2,  1,  0,  1,  2,  1,  0,  0,  0],
                [ -1,  0,  0,  0,  1,  2,  1,  0,  1,  1,  1,  0,  1,  2,  1,  0,  0,  0, -1],
                [ -1, -1,  0,  0,  0,  1,  2,  1,  0,  0,  0,  0,  1,  2,  1,  0,  0, -1, -1],
                [ -4, -1, -1,  0,  0,  0,  1,  2,  1,  2,  2,  1,  2,  1,  0,  0, -1, -1, -4],
                [ -6, -4, -2, -1,  0,  0,  0,  1,  3,  3,  3,  2,  1,  0,  0, -1, -1, -4, -6],
                [ -8, -6, -4, -1, -1, -1,  0,  0,  1,  2,  1,  1,  0,  0, -1, -1, -4, -6, -8],
                [-10, -8, -6, -4, -1, -1, -1,  0,  1,  1,  1,  0,  0,  0, -1, -4, -6, -8, -10]
            ])
    """
    print(np.sum(kernal))
    for i in range(len(kernal)):
        print(i,len(kernal[i]))
    """
    stride=1
    if len(image_array.shape)==3:
        image_array = np.mean(image_array, axis=2)
    output=convolve(image_array,kernal,stride)
    output_normalized = (output-np.min(output))/(np.max(output)-np.min(output)+1e-5)
    output_normalized = np.where(output_normalized>0.8,255,0)
    output_normalized = output_normalized.astype(np.uint8)
    result_image = Image.fromarray(output_normalized)
    result=np.column_stack(np.nonzero(output_normalized))
    result[:,0]+=kernal.shape[0]
    result[:,1]+=kernal.shape[1]
    return result
if __name__=="__main__":
    image = './photo/a.png'
    img = Image.open(image)
    image_array = np.array(img)
    detect_face(image_array)

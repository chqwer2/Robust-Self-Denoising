# import matplotlib.pyplot as plt
import cv2
import numpy as np


def standard_devide(img, Wfactor=4, Hfactor=3):
    h, w = img.shape[:2]
    w_length = int(w/Wfactor)
    h_length = int(h/Hfactor)
    # print(h_length, w_length)
    img_array = []
    for i in range(Hfactor):
        for j in range(Wfactor):
            img_array.append(img[i*h_length:(i+1)*h_length, 
                                 j*w_length:(j+1)*w_length].copy())
            
    return img_array


def overlap_devide(img, Wfactor=4, Hfactor=3, over_eps=4):
    h, w = img.shape[:2]
    w_length = int(w/Wfactor)
    h_length = int(h/Hfactor)
    
    img = np.asarray(cv2.copyMakeBorder(img, 0, over_eps, 0, over_eps, 
                             cv2.BORDER_CONSTANT, value=(0,0,0)))
    
    img_array = []
    
    for i in range(Hfactor):
        for j in range(Wfactor):
            img_cache = img[i*h_length : (i+1)*h_length+over_eps,
                                 j*w_length : (j+1)*w_length+over_eps].copy()
            
            # print(np.asarray(img_cache).shape, i*h_length, : (i+1)*h_length+over_eps)
            img_array.append(img_cache)
            
            
            
    return img_array

    
    
def combine_img(img_array, Wfactor=4, Hfactor=3, margin=5):
    # print(np.asarray(img_array).shape)
    h, w = img_array[0].shape[:2]

    img = np.ones((h*Hfactor + (Hfactor-1)*margin, 
                    w*Wfactor + (Wfactor-1)*margin, 3))*255
    
    
    for i in range(Hfactor):
        for j in range(Wfactor):
            img[i*margin+i*h : i*margin+(i+1)*h, 
                j*margin+j*w : j*margin+(j+1)*w] = img_array[i*Wfactor + j].copy()
    
    return img.astype(np.uint8)


def imread(img_file):
    return cv2.imread(img_file)

def padding(img, Wfactor=4, Hfactor=3, pad_value=0 ):
    h, w = img.shape[:2]
    h_pad = (Hfactor-h%Hfactor)%Hfactor
    w_pad = (Wfactor-w%Wfactor)%Wfactor
    # top, bottom, left, right
    ret = cv2.copyMakeBorder(img, 0, h_pad, 0, w_pad, cv2.BORDER_CONSTANT, value=(pad_value,pad_value,pad_value))
    return ret

if __name__ == '__main__':
    # Test the Result
    img = imread('/Users/haochen/Desktop/Robust-Self-Denoising/test_imgs/0045.png')
    pad_img = padding(img,pad_value=0)
    img_array = standard_devide(img)
    
    comb_img = combine_img(img_array, Wfactor=4, Hfactor=3, margin=5)
    img_over_array = overlap_devide(img, Wfactor=4, Hfactor=3, over_eps=15)
    comb_img_over = combine_img(img_over_array , Wfactor=4, Hfactor=3, margin=5)
    cv2.imshow("pad img", pad_img)
    cv2.imshow("com img", comb_img)
    cv2.imshow("com overlaped img", comb_img_over)
    
    cv2.imwrite("/Users/haochen/Desktop/Robust-Self-Denoising/cache_imgs/comb_img.jpg", comb_img)
    cv2.imwrite("/Users/haochen/Desktop/Robust-Self-Denoising/cache_imgs/omb_img_over.jpg", comb_img_over)
    
    cv2.waitKey(0)
    standard_devide(img)
    
    
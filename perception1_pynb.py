# -*- coding: utf-8 -*-
"""Perception1.pynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EMmhFozW0BLDAQa9USGZZlwwmQaK2ihi
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage, signal
from skimage import io, img_as_float
from scipy.signal import convolve2d

image_path = '/content/ques1.jpg'
image = img_as_float(io.imread(image_path))

def motion_blur_kernel(length):
    kernel = np.zeros((length, length))
    kernel[int((length - 1) / 2), :] = np.ones(length) / length
    return kernel

kernel_length = 40
motion_kernel = motion_blur_kernel(kernel_length)

blurred_r = convolve2d(image[:, :, 0], motion_kernel, boundary='wrap', mode='same')
blurred_g = convolve2d(image[:, :, 1], motion_kernel, boundary='wrap', mode='same')
blurred_b = convolve2d(image[:, :, 2], motion_kernel, boundary='wrap', mode='same')

motion_blurred_image = np.stack((blurred_r, blurred_g, blurred_b), axis=2)

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(image)
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(motion_blurred_image)
plt.title('Motion Blurred Image')
plt.axis('off')

plt.show()

motion_blurred_image_uint8 = (motion_blurred_image * 255).astype(np.uint8)
io.imsave('blurred_image.jpg', motion_blurred_image_uint8)

from scipy.fftpack import fft2, ifft2, fftshift

def wiener_filter(blurred, kernel, K=0.01):
    blurred_ft = fft2(blurred)
    kernel_ft = fft2(kernel,blurred.shape)

    kernel_ft_conj = np.conjugate(kernel_ft)
    numerator = kernel_ft_conj * blurred_ft
    denominator = (np.abs(kernel_ft) ** 2 + K)

    deblurred_ft = numerator / denominator

    deblurred = np.abs(ifft2(deblurred_ft))
    return deblurred

# Apply the Wiener filter to each color channel
deblurred_r = wiener_filter(motion_blurred_image[:, :, 0], motion_kernel)
deblurred_g = wiener_filter(motion_blurred_image[:, :, 1], motion_kernel)
deblurred_b = wiener_filter(motion_blurred_image[:, :, 2], motion_kernel)

# Stack the deblurred channels back into a color image
deblurred_image = np.stack((deblurred_r, deblurred_g, deblurred_b), axis=2)

# Plot the original blurred and deblurred images
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(motion_blurred_image)
plt.title('Blurred Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(deblurred_image)
plt.title('Deblurred Image (Wiener Filter)')
plt.axis('off')

plt.show()

deblurred_image_uint8 = (deblurred_image * 255).astype(np.uint8)
io.imsave('deblurred_image.jpg', deblurred_image_uint8)
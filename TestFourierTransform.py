import cv2
import numpy as np
import pyfftw
from cmath import exp, pi

# image = cv2.imread('Lenna.png', 0)
image_16 = (255 * np.random.randn(16, 16)).astype(np.uint8)
image_32 = (255 * np.random.randn(32, 32)).astype(np.uint8)
image_64 = (255 * np.random.randn(64, 64)).astype(np.uint8)
image_128 = (255 * np.random.randn(128, 128)).astype(np.uint8)
image_256 = (255 * np.random.randn(256, 256)).astype(np.uint8)
image_512 = (255 * np.random.randn(512, 512)).astype(np.uint8)

def ft_opencv(image):
    fourier = cv2.dft(image.astype(np.float32))
    fourier = np.fft.fftshift(fourier)
    return fourier

def ft_numpy(image):
    fourier = np.fft.fft2(image)
    fourier = np.fft.fftshift(fourier)
    return fourier

# pyfftw.interfaces.caches.enable()
def ft_fftw(image):
    N = image.shape[0] * image.shape[1]
    a = pyfftw.empty_aligned(N, dtype='complex128', n=16)
    a[:] = image.reshape((N))
    # b = pyfftw.interfaces.numpy_fft.fft(a)
    b = pyfftw.FFTW(a, b, axes=(0,1))
    return b

def ft_fft(image):
    N = len(image)
    if N <= 1: 
        return ft_numpy(image)
    even = ft_fft(image[0::2])
    odd =  ft_fft(image[1::2])
    T= [exp(-2j*pi*k/N)*odd[k] for k in range(N//2)]
    return [even[k] + T[k] for k in range(N//2)] + \
           [even[k] - T[k] for k in range(N//2)]

def ft_naive(image):
    N = image.shape[0]
    j = np.arange(N)
    k = j.reshape((N, 1))
    W = np.exp(-2j * np.pi * k * j / N)
    result = np.dot(np.dot(W, image), W)
    return np.fft.fftshift(result)

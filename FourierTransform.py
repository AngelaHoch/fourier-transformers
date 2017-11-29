import numpy as np

def forward(matrix):
    fourier = np.fft.fft2(matrix)
    fourier = np.fft.fftshift(fourier)
    return fourier

def normalize(fourier):
    fourier = np.abs(fourier)
    fourier = np.log(fourier)
    lowest = np.nanmin(fourier[np.isfinite(fourier)])
    highest = np.nanmax(fourier[np.isfinite(fourier)])
    org_range = highest - lowest
    normalize = (fourier - lowest) / org_range * 255
    return normalize.astype(np.uint8)

def inverse(fourier):
    fourier = np.fft.ifftshift(fourier)
    fourier = np.fft.ifft2(fourier)
    return  fourier

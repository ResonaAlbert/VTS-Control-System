import math
import numpy as np

#fit curve function
def order3curve(t0 = 0, T = 1, y0 = 0, y1 = 0, t = 0):
    t = t - t0
    y = y1 + (y1 - y0) * (t - T) ** 3 / T ** 3
    return y

def cos_fit_half(t0 = 0, T = 1, y0 = 0, y1 = 0, t = 0):
    t = t - t0
    y = (y0 + y1)/2 + ((y0 - y1)/2) * math.cos( math.pi * (t - t0) / T )
    return y

def cos_fit_full(t0 = 0, T = 1, y0 = 0, y1 = 0, t = 0, N = 1):
    t = t - t0
    y = (y0 + y1)/2 + ((y0 - y1)/2) * math.cos( 2 * N * math.pi * (t - t0) / T )
    return y

def sin_fit_full(t0 = 0, T = 1, y0 = 0, y1 = 0, t = 0, N = 1):
    t = t - t0
    y = ((y0 - y1)) * math.sin( 2 * N * math.pi * (t - t0) / T ) + y0
    return y

def cos_fun01(T0 = 0, T = 2, N = 5, t = 0):
    value = math.cos( 2 * N * math.pi * (t - T0) / T ) + 0.5
    return value

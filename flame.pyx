#cython: cdivision=True

cimport cython
cimport numpy as np
import numpy as np

np.import_array()
np.import_ufunc()


cdef extern from "stdlib.h":
    long random()
    long RAND_MAX


cdef extern from "math.h":
    double floor(double)
    double pow(double, double)
    double log(double)
    long lround(double)


cdef inline double random_sample():
    return random() / (RAND_MAX - 1.0)


cdef inline long random_integer(long low, long high):
    return low + <long>(random_sample() * (high - low + 1))


@cython.boundscheck(False)
@cython.wraparound(False)
def render_fractal(np.ndarray[np.uint8_t, ndim=3] pixels,
                   np.ndarray[np.uint32_t, ndim=2] counts,
                   np.ndarray[np.float64_t, ndim=2] maps,
                   np.ndarray[np.uint8_t, ndim=2] colors,
                   int width,
                   int height,
                   int max_iter):

    cdef:
        double x, y, _x, r, g, b
        Py_ssize_t i, n, m, idx, px, py

    n = len(maps)

    x = 1.0 - 2.0 * random_sample()
    y = 1.0 - 2.0 * random_sample()
    r, g, b = 0.0, 0.0, 0.0

    for i in range(max_iter):

        idx = random_integer(0, n - 1)
        _x = maps[idx, 0] * x + maps[idx, 1] * y + maps[idx, 4]
        y = maps[idx, 2] * x + maps[idx, 3] * y + maps[idx, 5]
        x = _x

        r = (r + colors[idx, 0]) * 0.5
        g = (g + colors[idx, 1]) * 0.5
        b = (b + colors[idx, 2]) * 0.5

        if i <= 20:
            continue

        px = lround((x + 1) * width / 2)
        py = lround((y + 1) * height / 2)

        if px < width and py < height and px >= 0 and py >= 0:
            counts[px, py] += 1

            pixels[px, py, 0] = <np.uint8_t>((counts[px, py] * pixels[px, py, 0] + r) / (counts[px, py] + 1))
            pixels[px, py, 1] = <np.uint8_t>((counts[px, py] * pixels[px, py, 1] + g) / (counts[px, py] + 1))
            pixels[px, py, 2] = <np.uint8_t>((counts[px, py] * pixels[px, py, 2] + b) / (counts[px, py] + 1))

    m = np.max(counts)

    for i in range(width):
        for j in range(height):
            if counts[i, j] > 0:
                pixels[i, j, 3] = <np.uint8_t>(floor(pow(log(1.0 + counts[i, j] * 1.0 / m) * 1.4426950408889634, 0.45) * 255))

    return pixels

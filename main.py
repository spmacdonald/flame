from random import randint

import png
import numpy as np

from flame import render_fractal


def generate_palette(n):

    min_color = 48
    max_color = 255

    colors = np.random.randint(min_color, max_color, (n, 3))
    return np.asarray(colors, dtype=np.uint8)


def random_sign(n):
    arr = np.random.random(n)
    arr[arr < 0.5] = -1
    arr[arr >= 0.5] = 1
    return arr


def generate_transformations(n):

    rot_angle_max = 2.0 * np.pi
    skew_angle_max = np.pi / 12.0
    scale_max = 1.0
    scale_min = 0.4

    rot_angle = (1.0 - 2.0 * np.random.random_sample(n)) * rot_angle_max
    skew_angle = (1.0 - 2.0 * np.random.random_sample(n) ** 3) * skew_angle_max
    angle_1 = rot_angle + skew_angle
    angle_2 = rot_angle - skew_angle

    rad_1 = random_sign(n) * (scale_min + np.random.random_sample(n) * (scale_max - scale_min))
    rad_2 = random_sign(n) * (scale_min + np.random.random_sample(n) * (scale_max - scale_min))

    x0 = rad_1 * np.cos(angle_1)
    y0 = rad_1 * np.sin(angle_1)
    x1 = -rad_2 * np.sin(angle_2)
    y1 = rad_2 * np.cos(angle_2)

    max_x = np.abs(x0) + np.abs(x1)
    x0[max_x > 1] /= max_x[max_x > 1]
    y0[max_x > 1] /= max_x[max_x > 1]
    x1[max_x > 1] /= max_x[max_x > 1]
    y1[max_x > 1] /= max_x[max_x > 1]

    max_y = np.abs(y0) + np.abs(y1)
    x0[max_y > 1] /= max_y[max_y > 1]
    y0[max_y > 1] /= max_y[max_y > 1]
    x1[max_y > 1] /= max_y[max_y > 1]
    y1[max_y > 1] /= max_y[max_y > 1]

    trans_x = np.random.random_sample(n) ** 0.5 * random_sign(n) * (1.0 - np.abs(x0) - np.abs(x1))
    trans_y = np.random.random_sample(n) ** 0.5 * random_sign(n) * (1.0 - np.abs(y0) - np.abs(y1))

    transformations = np.zeros((n, 6))
    transformations[:, 0] = x0
    transformations[:, 1] = x1
    transformations[:, 2] = y0
    transformations[:, 3] = y1
    transformations[:, 4] = trans_x
    transformations[:, 5] = trans_y

    return transformations


height = 500
width = 500
max_iter = 10000000
n = randint(4, 7)

pixels = np.zeros((width, height, 4), dtype=np.uint8)
counts = np.zeros((width, height), dtype=np.uint32)

colors = generate_palette(n)
maps = generate_transformations(n)

pixels = render_fractal(pixels, counts, maps, colors, width, height, max_iter)

# Composite pixels with a black background. See
# http://en.wikipedia.org/wiki/Alpha_compositing
alpha = np.index_exp[:, :, 3:]
rgb = np.index_exp[:, :, :3]
src_a = pixels[alpha] / 255.0
pixels[alpha] = 255
pixels[rgb] *= src_a
np.clip(pixels, 0, 255)

writer = png.Writer(width=width, height=height, alpha=True)
writer.write(open('image1.png', 'w'), pixels.reshape(-1, width * 4))

import os
import json
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


def composite_black_background(src):
    alpha = np.index_exp[:, :, 3:]
    rgb = np.index_exp[:, :, :3]
    src_a = src[alpha] / 255.0
    src[alpha] = 255
    src[rgb] *= src_a
    np.clip(src, 0, 255)

    return src


def write_parameters(fname, colors, maps):
    with open(fname, 'w') as f:
        parameters = {'colors': colors.tolist(), 'maps': maps.tolist()}
        json.dump(parameters, f)


def read_parameters(fname):
    with open(fname) as f:
        parameters = json.load(f)

    return {'maps': np.array(parameters['maps']),
            'colors': np.array(parameters['colors'], dtype=np.uint8)}


def search_fractals(height, width, quality, out_dir='/Volumes/internal/Datasets/flames', num=1000):

    max_iter = width * height * quality

    for i in range(num):
        n = randint(4, 10)

        pixels = np.zeros((height, width, 4), dtype=np.uint8)
        counts = np.zeros((height, width), dtype=np.uint32)

        colors = generate_palette(n)
        maps = generate_transformations(n)

        write_parameters(os.path.join(out_dir, '{0}.txt'.format(i)), colors, maps)

        pixels = render_fractal(pixels, counts, maps, colors, height, width, max_iter)
        pixels = composite_black_background(pixels)

        writer = png.Writer(width=width, height=height, alpha=True)
        writer.write(open(os.path.join(out_dir, '{0}.png'.format(i)), 'w'), pixels.reshape(-1, width * 4))


def generate_fractal(number, height=3000, width=3000, quality=30, out_dir='/Volumes/internal/Datasets/flames'):

    parameters = read_parameters(os.path.join(out_dir, '{0}.txt'.format(number)))
    colors = parameters['colors']
    maps = parameters['maps']

    max_iter = width * height * quality

    pixels = np.zeros((height, width, 4), dtype=np.uint8)
    counts = np.zeros((height, width), dtype=np.uint32)

    pixels = render_fractal(pixels, counts, maps, colors, height, width, max_iter)
    pixels = composite_black_background(pixels)

    writer = png.Writer(width=width, height=height, alpha=True)
    writer.write(open('{0}_high_quality.png'.format(number), 'w'), pixels.reshape(-1, width * 4))


if __name__ == '__main__':

    # width = 500
    # height = 500
    # quality = 30
    # search_fractals(height, width, quality)

    generate_fractal(1)


from random import random, randint
from math import floor, pow, log

import png
import numpy as np


# np.random.seed(0)


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


height = 1200
width = 1200

colors = generate_palette(4)
maps = generate_transformations(4)

# print maps
# colors = np.array([[241, 255, 130], [255, 123, 135], [255, 196, 69], [171, 255, 142]], dtype=np.uint8)
# maps = np.array([[-0.3041196177913254,
                  # 0.19183543928544902,
                  # -0.3081028290125658,
                  # -0.6918971709874343,
                  # -0.4458164517498235,
                  # -7.257607115881289e-17],
                 # [-0.35962699245997864,
                  # -0.6403730075400212,
                  # 0.6362672034320662,
                  # 0.005742118169683541,
                  # 7.810749347195336e-17,
                  # -0.13548979558696475],
                 # [-0.18681550921770365,
                  # 0.4220526475253291,
                  # -0.4339950726801396,
                  # -0.5660049273198604,
                  # 0.1779515243507741,
                  # 0.0],
                 # [0.6775626023138168,
                  # 0.32243739768618324,
                  # -0.2686837250960814,
                  # 0.2552858193518741,
                  # 3.683679486506543e-17,
                  # -0.2742142962730278]])


pixels = np.zeros((width, height, 4), dtype=np.uint8)
counts = np.zeros((width, height))

x = 1 - 2 * random()
y = 1 - 2 * random()
r, g, b = 0, 0, 0

for i in range(1000000L):
    idx = randint(0, len(maps) - 1)
    matrix = maps[idx]
    _x = matrix[0] * x + matrix[1] * y + matrix[4]
    y = matrix[2] * x + matrix[3] * y + matrix[5]
    x = _x

    color = colors[idx]
    r = (r + color[0]) * 0.5
    g = (g + color[1]) * 0.5
    b = (b + color[2]) * 0.5

    if i <= 20:
        continue

    px = round((x + 1) * width / 2)
    py = round((y + 1) * height / 2)

    if px < width and py < height and px >= 0 and py >= 0:
        counts[px][py] += 1

        pixels[px][py][0] = (counts[px][py] * pixels[px][py][0] + r) / (counts[px][py] + 1)
        pixels[px][py][1] = (counts[px][py] * pixels[px][py][1] + g) / (counts[px][py] + 1)
        pixels[px][py][2] = (counts[px][py] * pixels[px][py][2] + b) / (counts[px][py] + 1)

g = 1.4426950408889634
m = np.max(counts)

for i in range(width):
    for j in range(height):
        if counts[i][j] > 0:
            pixels[i][j][3] = floor(pow(log(1.0 + counts[i][j] * 1.0 / m) * g, 0.45) * 255)


# Composite pixels with a black background. See
# http://en.wikipedia.org/wiki/Alpha_compositing
alpha = np.index_exp[:, :, 3:]
rgb = np.index_exp[:, :, :3]
src_a = pixels[alpha] / 255.0
pixels[alpha] = 255
pixels[rgb] *= src_a
np.clip(pixels, 0, 255)

writer = png.Writer(width=width, height=height, alpha=True)
writer.write(open('flame.png', 'w'), pixels.reshape(-1, width * 4))

# Вспомогательная математика: векторы и матрицы
import math
import numpy as np


def normalize(v):
    length = math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
    if length == 0:
        return v
    return v / length


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def look_at(eye, target, up):
    # матрица вида: переводит мировые координаты в координаты камеры
    z = normalize(eye - target)  # камера смотрит вдоль -z
    x = normalize(np.cross(up, z))
    y = np.cross(z, x)

    m = np.identity(4)
    m[0, 0:3] = x
    m[1, 0:3] = y
    m[2, 0:3] = z
    m[0, 3] = -dot(x, eye)
    m[1, 3] = -dot(y, eye)
    m[2, 3] = -dot(z, eye)
    return m


def perspective(fov_deg, aspect, near, far):
    # матрица перспективной проекции (как в OpenGL)
    f = 1.0 / math.tan(math.radians(fov_deg) / 2)
    m = np.zeros((4, 4))
    m[0, 0] = f / aspect
    m[1, 1] = f
    m[2, 2] = (far + near) / (near - far)
    m[2, 3] = (2 * far * near) / (near - far)
    m[3, 2] = -1
    return m


def viewport(width, height):
    # переводит координаты из [-1, 1] в пиксели экрана
    m = np.identity(4)
    m[0, 0] = width / 2
    m[0, 3] = width / 2
    m[1, 1] = -height / 2  # ось y у картинки идёт вниз, поэтому минус
    m[1, 3] = height / 2
    return m

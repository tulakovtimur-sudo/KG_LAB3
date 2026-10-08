# Класс камеры
import numpy as np
from mymath import look_at, perspective


class Camera:
    def __init__(self, position, target, up, fov, aspect, near=0.1, far=100.0):
        self.position = np.array(position, dtype=float)  # где стоит камера
        self.target = np.array(target, dtype=float)      # куда смотрит
        self.up = np.array(up, dtype=float)              # где у камеры "верх"
        self.fov = fov          # угол обзора в градусах
        self.aspect = aspect    # ширина / высота
        self.near = near
        self.far = far

    def get_view_matrix(self):
        return look_at(self.position, self.target, self.up)

    def get_projection_matrix(self):
        return perspective(self.fov, self.aspect, self.near, self.far)

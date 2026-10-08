# Шейдеры: вершинный и фрагментный (пиксельный)
import numpy as np
from mymath import normalize, dot


class PhongShader:
    def __init__(self, model, view, projection, viewport_m, camera_pos, light_dir, texture=None):
        self.model = model
        self.mvp = projection @ view  # матрица модели у нас единичная, поэтому её не пишем
        self.viewport = viewport_m
        self.camera_pos = camera_pos
        self.light_dir = normalize(np.array(light_dir, dtype=float))  # направление НА источник света
        self.texture = texture  # картинка текстуры (numpy массив) или None

        if texture is not None:
            self.tex_h = texture.shape[0]
            self.tex_w = texture.shape[1]

        # параметры освещения по Фонгу
        self.ambient = 0.15
        self.diffuse = 0.8
        self.specular = 0.4
        self.shininess = 32
        self.base_color = np.array([200, 200, 200], dtype=float)  # цвет если нет текстуры

        # данные трёх вершин текущего треугольника (их потом интерполируем)
        self.world_pos = [None, None, None]
        self.normals = [None, None, None]
        self.uvs = [None, None, None]

    def vertex(self, face, i):
        # вершинный шейдер: обрабатывает i-ю вершину треугольника
        v_idx, vt_idx, vn_idx = face[i]

        pos = np.array(self.model.vertices[v_idx])
        self.world_pos[i] = pos

        if vn_idx >= 0:
            self.normals[i] = normalize(np.array(self.model.normals[vn_idx]))
        else:
            self.normals[i] = None

        if vt_idx >= 0:
            self.uvs[i] = self.model.texcoords[vt_idx]
        else:
            self.uvs[i] = [0, 0]

        # переводим в однородные координаты и умножаем на матрицы
        p = np.array([pos[0], pos[1], pos[2], 1.0])
        clip = self.mvp @ p
        ndc = clip / clip[3]  # перспективное деление
        screen = self.viewport @ ndc
        return screen  # x, y - пиксели, z - глубина

    def fragment(self, a, b, c):
        # фрагментный шейдер: считает цвет пикселя
        # a, b, c - барицентрические координаты пикселя

        # интерполируем позицию и нормаль
        pos = self.world_pos[0] * a + self.world_pos[1] * b + self.world_pos[2] * c
        if self.normals[0] is not None:
            n = self.normals[0] * a + self.normals[1] * b + self.normals[2] * c
            n = normalize(n)
        else:
            # если нормалей нет в файле - считаем нормаль треугольника
            e1 = self.world_pos[1] - self.world_pos[0]
            e2 = self.world_pos[2] - self.world_pos[0]
            n = normalize(np.cross(e1, e2))

        # цвет поверхности: из текстуры или просто серый
        if self.texture is not None:
            u = self.uvs[0][0] * a + self.uvs[1][0] * b + self.uvs[2][0] * c
            v = self.uvs[0][1] * a + self.uvs[1][1] * b + self.uvs[2][1] * c
            tx = int(u * (self.tex_w - 1))
            ty = int((1 - v) * (self.tex_h - 1))  # в картинке y сверху вниз, поэтому 1 - v
            tx = min(max(tx, 0), self.tex_w - 1)
            ty = min(max(ty, 0), self.tex_h - 1)
            color = self.texture[ty, tx].astype(float)
        else:
            color = self.base_color

        # освещение по Фонгу
        l = self.light_dir
        view_dir = normalize(self.camera_pos - pos)

        diff = max(dot(n, l), 0)

        # отражённый луч: r = 2 * (n * l) * n - l
        r = normalize(2 * dot(n, l) * n - l)
        spec = 0
        if diff > 0:
            spec = max(dot(r, view_dir), 0) ** self.shininess

        result = color * (self.ambient + self.diffuse * diff) + 255 * self.specular * spec
        result = np.clip(result, 0, 255)
        return result

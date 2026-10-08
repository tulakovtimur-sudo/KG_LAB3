# Растеризатор на барицентрических координатах
import math


def barycentric(x, y, p0, p1, p2):
    # считаем барицентрические координаты точки (x, y) относительно треугольника
    area = (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1])
    if abs(area) < 1e-9:
        return -1, -1, -1  # вырожденный треугольник
    b = ((x - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (y - p0[1])) / area
    c = ((p1[0] - p0[0]) * (y - p0[1]) - (x - p0[0]) * (p1[1] - p0[1])) / area
    a = 1 - b - c
    return a, b, c


def draw_triangle(pts, shader, image, zbuffer):
    # pts - три точки на экране (x, y, z)
    width = image.shape[1]
    height = image.shape[0]

    # ограничивающий прямоугольник треугольника
    min_x = max(0, int(math.floor(min(pts[0][0], pts[1][0], pts[2][0]))))
    max_x = min(width - 1, int(math.ceil(max(pts[0][0], pts[1][0], pts[2][0]))))
    min_y = max(0, int(math.floor(min(pts[0][1], pts[1][1], pts[2][1]))))
    max_y = min(height - 1, int(math.ceil(max(pts[0][1], pts[1][1], pts[2][1]))))

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            # берём центр пикселя
            a, b, c = barycentric(x + 0.5, y + 0.5, pts[0], pts[1], pts[2])
            if a < 0 or b < 0 or c < 0:
                continue  # пиксель снаружи треугольника

            # глубина пикселя
            z = pts[0][2] * a + pts[1][2] * b + pts[2][2] * c

            # z-буфер: рисуем только если пиксель ближе того что уже нарисован
            if z < zbuffer[y, x]:
                zbuffer[y, x] = z
                image[y, x] = shader.fragment(a, b, c)

# Главный файл: загружаем модель, ставим камеру и рендерим в картинку
import time
import numpy as np
from PIL import Image

from obj_loader import Model
from camera import Camera
from mymath import viewport, dot, normalize
from shaders import PhongShader
from rasterizer import draw_triangle

# ===== Настройки =====
WIDTH = 800
HEIGHT = 800
MODEL_FILE = "models/african_head.obj"
TEXTURE_FILE = "models/african_head_diffuse.tga"  # поставь None чтобы рендерить без текстуры
OUTPUT_FILE = "output.png"
LIGHT_DIR = [1, 1, 1]  # направление на источник света


def main():
    start = time.time()

    model = Model(MODEL_FILE)

    texture = None
    if TEXTURE_FILE is not None:
        texture = np.array(Image.open(TEXTURE_FILE).convert("RGB"))
        print("Текстура:", texture.shape[1], "x", texture.shape[0])

    camera = Camera(position=[1, 1, 3], target=[0, 0, 0], up=[0, 1, 0],
                    fov=45, aspect=WIDTH / HEIGHT)

    view = camera.get_view_matrix()
    projection = camera.get_projection_matrix()
    vp = viewport(WIDTH, HEIGHT)

    shader = PhongShader(model, view, projection, vp, camera.position, LIGHT_DIR, texture)

    # картинка (фон тёмно-серый) и z-буфер (сначала всё бесконечно далеко)
    image = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    image[:, :] = [40, 40, 40]
    zbuffer = np.full((HEIGHT, WIDTH), np.inf)

    count = 0
    for face in model.faces:
        pts = []
        for i in range(3):
            pts.append(shader.vertex(face, i))

        # отбрасываем треугольники которые смотрят от камеры (back-face culling)
        e1 = shader.world_pos[1] - shader.world_pos[0]
        e2 = shader.world_pos[2] - shader.world_pos[0]
        face_normal = normalize(np.cross(e1, e2))
        if dot(face_normal, camera.position - shader.world_pos[0]) <= 0:
            continue

        draw_triangle(pts, shader, image, zbuffer)

        count += 1
        if count % 500 == 0:
            print("Нарисовано треугольников:", count)

    Image.fromarray(image).save(OUTPUT_FILE)
    print("Готово! Сохранено в", OUTPUT_FILE)
    print("Время:", round(time.time() - start, 1), "сек")


if __name__ == "__main__":
    main()

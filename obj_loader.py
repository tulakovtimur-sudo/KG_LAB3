# Загрузчик .obj файлов (свой парсер)
# Читаем вершины (v), текстурные координаты (vt), нормали (vn) и грани (f)


class Model:
    def __init__(self, filename):
        self.vertices = []   # список [x, y, z]
        self.texcoords = []  # список [u, v]
        self.normals = []    # список [nx, ny, nz]
        self.faces = []      # каждая грань - список из 3 вершин, вершина = (индекс_v, индекс_vt, индекс_vn)

        self.load(filename)

    def load(self, filename):
        f = open(filename, "r")
        for line in f:
            parts = line.split()
            if len(parts) == 0:
                continue

            if parts[0] == "v":
                x = float(parts[1])
                y = float(parts[2])
                z = float(parts[3])
                self.vertices.append([x, y, z])

            elif parts[0] == "vt":
                u = float(parts[1])
                v = float(parts[2])
                self.texcoords.append([u, v])

            elif parts[0] == "vn":
                nx = float(parts[1])
                ny = float(parts[2])
                nz = float(parts[3])
                self.normals.append([nx, ny, nz])

            elif parts[0] == "f":
                face = []
                for p in parts[1:]:
                    # формат может быть v, v/vt, v//vn или v/vt/vn
                    nums = p.split("/")
                    v_idx = int(nums[0]) - 1  # в obj индексы с 1, а в питоне с 0
                    vt_idx = -1
                    vn_idx = -1
                    if len(nums) > 1 and nums[1] != "":
                        vt_idx = int(nums[1]) - 1
                    if len(nums) > 2 and nums[2] != "":
                        vn_idx = int(nums[2]) - 1
                    face.append((v_idx, vt_idx, vn_idx))

                # если грань не треугольник (например квадрат), режем на треугольники
                for i in range(1, len(face) - 1):
                    self.faces.append([face[0], face[i], face[i + 1]])
        f.close()

        print("Загружено вершин:", len(self.vertices))
        print("Загружено треугольников:", len(self.faces))

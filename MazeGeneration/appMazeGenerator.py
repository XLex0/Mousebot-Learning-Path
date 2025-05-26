import numpy as np
import random
import os

# definimos algoritmos para generar, en base a lo que se ha explicado en los 
# cuadernos jupyter

#Prim, laberintos con pasillos no tan profundos
def generar_laberinto_prim(n, m):
    if n % 2 == 0: n += 1
    if m % 2 == 0: m += 1
    maze = np.ones((n, m), dtype=int)

    def vecinos_validos(x, y):
        vecinos = []
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and maze[nx][ny] == 1:
                vecinos.append((nx, ny, x, y))
        return vecinos

    x, y = random.randrange(1, n, 2), random.randrange(1, m, 2)
    maze[x][y] = 0
    paredes = vecinos_validos(x, y)

    while paredes:
        idx = random.randint(0, len(paredes) - 1)
        px, py, ox, oy = paredes.pop(idx)
        if maze[px][py] == 1:
            maze[px][py] = 0
            maze[(px + ox)//2][(py + oy)//2] = 0
            paredes.extend(vecinos_validos(px, py))

    return maze


# Kruskal, laberintos que se combinan
class UnionFind:
    def __init__(self, n, m):
        self.parent = {(i, j): (i, j) for i in range(n) for j in range(m)}

    def find(self, cell):
        if self.parent[cell] != cell:
            self.parent[cell] = self.find(self.parent[cell])
        return self.parent[cell]

    def union(self, a, b):
        rootA = self.find(a)
        rootB = self.find(b)
        if rootA != rootB:
            self.parent[rootB] = rootA
            return True
        return False

def generar_laberinto_kruskal(n, m):
    if n % 2 == 0: n += 1
    if m % 2 == 0: m += 1
    maze = np.ones((n, m), dtype=int)
    celdas = [(i, j) for i in range(1, n, 2) for j in range(1, m, 2)]
    for x, y in celdas:
        maze[x][y] = 0
    muros = []
    for x, y in celdas:
        for dx, dy in [(2, 0), (0, 2)]:
            nx, ny = x + dx, y + dy
            if nx < n and ny < m:
                muros.append(((x, y), (nx, ny)))
    random.shuffle(muros)
    uf = UnionFind(n, m)
    for (a, b) in muros:
        if uf.union(a, b):
            mx, my = (a[0] + b[0]) // 2, (a[1] + b[1]) // 2
            maze[mx][my] = 0
    return maze

#laberintos con pasillos largos y profundos
def generar_laberinto_backtracking(n, m):
    if n % 2 == 0: n += 1
    if m % 2 == 0: m += 1
    maze = np.ones((n, m), dtype=int)
    def backtrack(x, y):
        maze[x][y] = 0
        dirs = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 < nx < n and 0 < ny < m and maze[nx][ny] == 1:
                maze[(x + nx) // 2][(y + ny) // 2] = 0
                backtrack(nx, ny)
    start_x, start_y = random.randrange(1, n, 2), random.randrange(1, m, 2)
    backtrack(start_x, start_y)
    return maze

# guardar como CSV
def guardar_laberinto(maze, nombre_base):
    np.savetxt(f"{nombre_base}.csv", maze, fmt="%d", delimiter=",")

def main():
    num_laberintos = int(input("¿Cuántos laberintos deseas generar? "))
    filas = int(input("Número de filas del laberinto: "))
    columnas = int(input("Número de columnas del laberinto: "))
    algoritmo = input("¿Qué algoritmo deseas usar? (prim / kruskal / backtracking): ").strip().lower()

    #carpeta donde se guarda los laberintos
    os.makedirs("laberintos_generados", exist_ok=True)

    for i in range(num_laberintos):
        if algoritmo == "prim":
            lab = generar_laberinto_prim(filas, columnas)
        elif algoritmo == "kruskal":
            lab = generar_laberinto_kruskal(filas, columnas)
        elif algoritmo == "backtracking":
            lab = generar_laberinto_backtracking(filas, columnas)
        else:
            print("Algoritmo no reconocido.")
            return

        base = f"laberintos_generados/laberinto_{algoritmo}_{i+1}"
        guardar_laberinto(lab, base)
        print(f"Laberinto {i+1} guardado en {base}.csv")

if __name__ == "__main__":
    main()

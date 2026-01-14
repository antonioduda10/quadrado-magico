import random

def generate_standard_magic_square():
    """
    Gera um quadrado mágico 3x3 padrão, usando 1 a 9.
    """
    return [
        [8, 1, 6],
        [3, 5, 7],
        [4, 9, 2]
    ]

def rotate_right(square):
    # Gira o quadrado 90 graus à direita
    return [
        [square[2][0], square[1][0], square[0][0]],
        [square[2][1], square[1][1], square[0][1]],
        [square[2][2], square[1][2], square[0][2]],
    ]

def flip_horizontal(square):
    # Espelha horizontalmente (de cima para baixo)
    return [square[2], square[1], square[0]]

def flip_vertical(square):
    # Espelha verticalmente (da esquerda para a direita)
    return [row[::-1] for row in square]

def get_all_magic_square_transforms(square):
    # Retorna todas as 8 rotações/espelhamentos possíveis
    transforms = []
    s = square
    for i in range(4):
        transforms.append(s)
        transforms.append(flip_horizontal(s))
        s = rotate_right(s)
    return transforms

def generate_magic_square_with_range(min_n, max_n):
    """
    Tenta gerar um quadrado mágico 3x3 com números no intervalo [min_n, max_n].
    Não é garantido que existam soluções para qualquer intervalo.
    (Atenção: Na prática, só alguns intervalos permitem solução mágica.)
    """
    nums = list(range(min_n, max_n + 1))
    if len(nums) < 9:
        raise ValueError("Intervalo muito pequeno para 3x3!")
    attempts = 10000
    for _ in range(attempts):
        square = random.sample(nums, 9)
        ms = [square[0:3], square[3:6], square[6:9]]
        magic_sum = sum(ms[0])
        if all(sum(row) == magic_sum for row in ms) and \
           all(sum(ms[i][j] for i in range(3)) == magic_sum for j in range(3)) and \
           sum(ms[i][i] for i in range(3)) == magic_sum and \
           sum(ms[i][2-i] for i in range(3)) == magic_sum:
            return ms
    raise ValueError("Não foi possível gerar um quadrado mágico com esse intervalo.")

def generate_magic_square(allow_negatives=False):
    """
    Gera quadrado mágico padrão (1-9) ou tenta aleatório no intervalo -9 a 9 se permitido negativos.
    """
    if not allow_negatives:
        return generate_standard_magic_square()
    else:
        return generate_magic_square_with_range(-9, 9)

def generate_magic_square_by_start(start):
    """
    Gera um quadrado mágico 3x3 usando números consecutivos de start a start+8,
    sortea uma das 8 rotações/espelhamentos possíveis a cada chamada.
    """
    base_square = generate_standard_magic_square()
    # Aplica transformação aleatória (rotação ou espelhamento)
    all_transforms = get_all_magic_square_transforms(base_square)
    chosen = random.choice(all_transforms)
    # Aplica o offset
    X = start - 1
    new_square = [[cell + X for cell in row] for row in chosen]
    return new_square

def generate_random_magic_square(allow_negatives=False):
    """
    Gera um quadrado mágico aleatório, apenas mudando sinal e offset (mantendo padrão matemático).
    Para 3x3, todo quadrado mágico pode ser obtido multiplicando e somando ao padrão.
    """
    base = generate_standard_magic_square()
    if allow_negatives:
        offset = random.randint(-20, 20)
        sign = random.choice([-1, 1])
    else:
        offset = random.randint(0, 20)
        sign = 1
    # Aplica rotação/espelhamento aleatório
    all_transforms = get_all_magic_square_transforms(base)
    chosen = random.choice(all_transforms)
    # Gera o quadrado mágico com offset e sinal
    return [[sign * cell + offset for cell in row] for row in chosen]

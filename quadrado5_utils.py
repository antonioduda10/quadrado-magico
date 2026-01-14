import random

def magic_sum(n, start=1):
    # Soma mágica correta para qualquer n e qualquer start
    return n * (n * n + 1) // 2 + (start - 1) * n

def magic_square_odd(n, start=1):
    # Quadrado mágico de ordem ímpar (Siamese method)
    square = [[0]*n for _ in range(n)]
    num = start
    i, j = 0, n // 2
    for _ in range(n*n):
        square[i][j] = num
        num += 1
        newi, newj = (i-1)%n, (j+1)%n
        if square[newi][newj]:
            i = (i+1)%n
        else:
            i, j = newi, newj
    return square

def magic_square_doubly_even(n, start=1):
    # Quadrado mágico de ordem n múltiplo de 4 (Strachey method)
    square = [[(i * n) + j + start for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if (i % 4 == j % 4) or ((i % 4 + j % 4) == 3):
                # Inverte o valor da célula de acordo com o padrão das diagonais
                square[i][j] = (start + n * n - 1) - (i * n + j)
    return square

def magic_square_singly_even(n, start=1):
    """
    Constrói quadrados mágicos para ordens n onde n % 4 == 2 (singly even).
    Implementação padrão via subquadrado ímpar de ordem n/2, com trocas de
    colunas conforme o método clássico (Strachey/Kraitchik).
    """
    if n % 4 != 2 or n < 6:
        raise ValueError("Ordem inválida para quadrado magicamente singular (n % 4 deve ser 2 e n >= 6)")

    m = n // 2  # ordem do subquadrado (ímpar)
    k = (n - 2) // 4  # número de colunas de troca

    sub = magic_square_odd(m, 1)
    add = m * m

    square = [[0] * n for _ in range(n)]

    # Monta quadrantes básicos
    for i in range(m):
        for j in range(m):
            square[i][j] = sub[i][j]                     # A
            square[i + m][j] = sub[i][j] + 3 * add       # C
            square[i][j + m] = sub[i][j] + 2 * add       # B
            square[i + m][j + m] = sub[i][j] + add       # D

    # Troca colunas à esquerda entre A/C e B/D
    for i in range(m):
        for j in range(k):
            square[i][j], square[i + m][j] = square[i + m][j], square[i][j]

    # Troca colunas à direita (últimas k-1 colunas) entre A/C e B/D
    for i in range(m):
        for j in range(n - k + 1, n):
            square[i][j], square[i + m][j] = square[i + m][j], square[i][j]

    # Trocas especiais para coluna k
    square[k][0], square[k + m][0] = square[k + m][0], square[k][0]
    square[k][k], square[k + m][k] = square[k + m][k], square[k][k]

    # Aplica offset de início
    if start != 1:
        offset = start - 1
        square = [[cell + offset for cell in row] for row in square]

    return square

def generate_magic_square_n(n, start=1):
    if n < 3:
        raise ValueError("Ordem deve ser pelo menos 3")
    if n % 2 == 1:
        return magic_square_odd(n, start)
    elif n % 4 == 0:
        return magic_square_doubly_even(n, start)
    else:
        return magic_square_singly_even(n, start)

def rotate_right(square):
    n = len(square)
    return [[square[n - 1 - j][i] for j in range(n)] for i in range(n)]

def flip_horizontal(square):
    return list(reversed(square))

def flip_vertical(square):
    return [list(reversed(row)) for row in square]

def get_all_magic_square_transforms(square):
    n = len(square)
    transforms = []
    s = square
    for i in range(4):
        transforms.append(s)
        transforms.append(flip_horizontal(s))
        s = rotate_right(s)
    return transforms

def escolher_indices_visiveis(qtd, n):
    total = n * n
    indices = list(range(total))
    random.shuffle(indices)
    return indices[:qtd]

def gerar_quadrado5_desafio(n, start, qtd):
    base = generate_magic_square_n(n, start)
    # Permutação aleatória (rotaciona/espelha)
    all_transforms = get_all_magic_square_transforms(base)
    permutado = random.choice(all_transforms)
    indices_visiveis = escolher_indices_visiveis(qtd, n)
    return permutado, indices_visiveis, magic_sum(n, start)

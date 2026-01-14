// Funcoes utilitarias para gerar quadrados magicos no lado do cliente (para GitHub Pages)

function baseMagicSquare3() {
    return [
        [8, 1, 6],
        [3, 5, 7],
        [4, 9, 2]
    ];
}

function rotateRight(square) {
    const n = square.length;
    const out = Array.from({ length: n }, () => Array(n).fill(0));
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            out[j][n - 1 - i] = square[i][j];
        }
    }
    return out;
}

function flipHorizontal(square) {
    return [...square].reverse();
}

function flipVertical(square) {
    return square.map(row => [...row].reverse());
}

function getAllMagicSquareTransforms(square) {
    const transforms = [];
    let current = square;
    for (let i = 0; i < 4; i++) {
        transforms.push(current);
        transforms.push(flipHorizontal(current));
        current = rotateRight(current);
    }
    return transforms;
}

function generateMagicSquareByStart(start = 1) {
    const base = baseMagicSquare3();
    const transforms = getAllMagicSquareTransforms(base);
    const chosen = transforms[Math.floor(Math.random() * transforms.length)];
    const offset = Number(start || 1) - 1;
    return chosen.map(row => row.map(cell => cell + offset));
}

function magicSum(n, start = 1) {
    return n * (n * n + 1) / 2 + (start - 1) * n;
}

function magicSquareOdd(n, start = 1) {
    const square = Array.from({ length: n }, () => Array(n).fill(0));
    let num = start;
    let i = 0;
    let j = Math.floor(n / 2);
    for (let k = 0; k < n * n; k++) {
        square[i][j] = num++;
        const newI = (i - 1 + n) % n;
        const newJ = (j + 1) % n;
        if (square[newI][newJ] !== 0) {
            i = (i + 1) % n;
        } else {
            i = newI;
            j = newJ;
        }
    }
    return square;
}

function magicSquareDoublyEven(n, start = 1) {
    const square = Array.from({ length: n }, () => Array(n).fill(0));
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            square[i][j] = (i * n) + j + start;
        }
    }
    const maxVal = start + n * n - 1;
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            if ((i % 4 === j % 4) || (((i % 4) + (j % 4)) === 3)) {
                square[i][j] = maxVal - (i * n + j);
            }
        }
    }
    return square;
}

function magicSquareSinglyEven(n, start = 1) {
    if (n % 4 !== 2 || n < 6) {
        throw new Error("Ordem invalida para quadrado singular (n % 4 deve ser 2 e n >= 6)");
    }
    const m = n / 2;
    const k = (n - 2) / 4;
    const sub = magicSquareOdd(m, 1);
    const add = m * m;
    const square = Array.from({ length: n }, () => Array(n).fill(0));

    for (let i = 0; i < m; i++) {
        for (let j = 0; j < m; j++) {
            square[i][j] = sub[i][j];
            square[i + m][j] = sub[i][j] + 3 * add;
            square[i][j + m] = sub[i][j] + 2 * add;
            square[i + m][j + m] = sub[i][j] + add;
        }
    }

    for (let i = 0; i < m; i++) {
        for (let j = 0; j < k; j++) {
            const tmp = square[i][j];
            square[i][j] = square[i + m][j];
            square[i + m][j] = tmp;
        }
    }

    for (let i = 0; i < m; i++) {
        for (let j = n - k + 1; j < n; j++) {
            const tmp = square[i][j];
            square[i][j] = square[i + m][j];
            square[i + m][j] = tmp;
        }
    }

    const tmp1 = square[k][0];
    square[k][0] = square[k + m][0];
    square[k + m][0] = tmp1;

    const tmp2 = square[k][k];
    square[k][k] = square[k + m][k];
    square[k + m][k] = tmp2;

    if (start !== 1) {
        const offset = start - 1;
        for (let i = 0; i < n; i++) {
            for (let j = 0; j < n; j++) {
                square[i][j] += offset;
            }
        }
    }
    return square;
}

function generateMagicSquareN(n, start = 1) {
    if (n < 3) {
        throw new Error("Ordem deve ser pelo menos 3");
    }
    if (n % 2 === 1) return magicSquareOdd(n, start);
    if (n % 4 === 0) return magicSquareDoublyEven(n, start);
    return magicSquareSinglyEven(n, start);
}

function chooseVisibleIndices(qtd, n) {
    const total = n * n;
    const maxQtd = Math.max(1, Math.min(qtd, total));
    const indices = Array.from({ length: total }, (_, i) => i);
    for (let i = indices.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [indices[i], indices[j]] = [indices[j], indices[i]];
    }
    return indices.slice(0, maxQtd);
}

function gerarQuadrado5Desafio(n, start, qtd) {
    const base = generateMagicSquareN(n, start);
    const transforms = getAllMagicSquareTransforms(base);
    const permutado = transforms[Math.floor(Math.random() * transforms.length)];
    const visiveis = chooseVisibleIndices(qtd, n);
    return {
        quadrado: permutado,
        visiveis,
        soma: magicSum(n, start)
    };
}

if (typeof window !== "undefined") {
    window.generateMagicSquareByStart = generateMagicSquareByStart;
    window.generateMagicSquareN = generateMagicSquareN;
    window.magicSum = magicSum;
    window.gerarQuadrado5Desafio = gerarQuadrado5Desafio;
    window.chooseVisibleIndices = chooseVisibleIndices;
}

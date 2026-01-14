from flask import Flask, render_template, request, jsonify
from quadrado_magico import generate_magic_square_by_start, generate_random_magic_square
from quadrado5_utils import gerar_quadrado5_desafio

app = Flask(__name__)

@app.route('/')
def pagina_inicial():
    return render_template('pagina_inicial.html')

@app.route('/quadrado1')
def quadrado1():
    return render_template('quadrado1.html')

@app.route('/quadrado2')
def quadrado2():
    return render_template('quadrado2.html')

@app.route('/quadrado3')
def quadrado3():
    return render_template('quadrado3.html')

@app.route('/quadrado4')
def quadrado4():
    return render_template('quadrado4.html')

@app.route('/quadrado5')
def quadrado5():
    return render_template('quadrado5.html')

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404

# Geração automática com opções (negativos)
@app.route('/generate_random', methods=['POST'])
def generate_random():
    data = request.get_json() or {}
    allow_negatives = data.get('allow_negatives', False)
    try:
        square = generate_random_magic_square(allow_negatives)
        magic_sum = sum(square[0])
        return jsonify({"success": True, "square": square, "magic_sum": magic_sum})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# Geração tradicional pelo número inicial
@app.route('/generate', methods=['POST'])
def generate():
    try:
        start = int(request.form.get('start', 1))
        square = generate_magic_square_by_start(start)
        magic_sum = sum(square[0])
        return jsonify({"success": True, "square": square, "magic_sum": magic_sum, "start": start, "end": start + 8})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# NOVA ROTA ADEQUADA PARA QUADRADO5 COM ORDEM n E PERMUTAÇÃO
@app.route("/quadrado5/desafio", methods=["POST"])
def quadrado5_desafio():
    data = request.get_json()
    n = int(data.get("n", 3))         # Ordem do quadrado (3, 4, 5, ...)
    start = int(data.get("start", 1))
    qtd = int(data.get("qtd", 3))
    quadrado, visiveis, soma = gerar_quadrado5_desafio(n, start, qtd)
    return jsonify({
        "quadrado": quadrado,
        "visiveis": visiveis,
        "n": n,
        "soma": soma
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

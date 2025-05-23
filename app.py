from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spin')
def spin():
    # Gera valores para 3 linhas e 3 colunas
    matrix = [
        [random.randint(1, 7) for _ in range(3)],  # topo
        [random.randint(1, 7) for _ in range(3)],  # meio
        [random.randint(1, 7) for _ in range(3)]   # base
    ]
    # verifica vitória na linha do meio
    win = (matrix[1] == [7, 7, 7])
    return jsonify({
        'matrix': matrix,
        'win': win
    })

if __name__ == '__main__':
    app.run(debug=True)
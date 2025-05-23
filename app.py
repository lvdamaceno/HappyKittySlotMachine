from flask import Flask, render_template, jsonify, session
import random

app = Flask(__name__)
# Chave para sessões (modifique para algo seguro em produção)
app.secret_key = 'sua_chave_secreta_aqui'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spin')
def spin():
    # Contabiliza jogadas na sessão do usuário
    plays = session.get('plays', 0) + 1
    session['plays'] = plays

    # Força vitória na décima jogada de cada dez
    if plays % 10 == 0:
        mid = [7, 7, 7]
    else:
        mid = [random.randint(1, 7) for _ in range(3)]

    # Cálculo com wrap circular para topo e base
    top = [(m - 1 if m > 1 else 7) for m in mid]
    bottom = [(m + 1 if m < 7 else 1) for m in mid]
    matrix = [top, mid, bottom]

    win = all(val == 7 for val in mid)
    return jsonify({'matrix': matrix, 'win': win})

if __name__ == '__main__':
    app.run(debug=True)
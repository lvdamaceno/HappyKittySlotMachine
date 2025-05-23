from flask import Flask, render_template, jsonify, session
import random
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

@app.route('/')
def index():
    if os.environ.get('FLASK_ENV') == 'development':
        session['coins'] = 1000
    elif 'coins' not in session:
        session['coins'] = 1000
    return render_template('index.html', coins=session['coins'])

@app.route('/spin')
def spin():
    coins = session.get('coins', 0)
    if coins < 100:
        return jsonify({ 'error': 'Sem moedas para jogar.', 'coins': coins })

    coins -= 100
    win = random.random() < 0.05
    if win:
        mid = [7, 7, 7]
    else:
        mid = [random.randint(1, 7) for _ in range(3)]

    top = [(m - 1 if m > 1 else 7) for m in mid]
    bottom = [(m + 1 if m < 7 else 1) for m in mid]
    matrix = [top, mid, bottom]

    bonus = 50 if any(val == 3 for row in matrix for val in row) else 0
    coins += bonus

    session['coins'] = coins
    return jsonify({
        'matrix': matrix,
        'win': win,
        'bonus': bonus,
        'coins': coins
    })

if __name__ == '__main__':
    app.run(debug=True)
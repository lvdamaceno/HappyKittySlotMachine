from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    message = ''
    if request.method == 'POST':
        # Gira os 3 rolos com números de 1 a 7
        results = [random.randint(1, 7) for _ in range(3)]
        # Verifica vitória (todos 7)
        if results.count(7) == 3:
            message = '🎉 Você ganhou! Parabéns!'
        else:
            message = 'Tente novamente.'
    return render_template('index.html', results=results, message=message)

if __name__ == '__main__':
    app.run(debug=True)
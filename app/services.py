import random
from app.models import Pontos, Jogadas, RegistroJogada
from app.extensions import db
from flask import current_app
from datetime import datetime

FIGURES = ['1', '2', '3', '4', '5', '6', '7']


class GameService:
    @staticmethod
    def spin(cpf):
        pts = Pontos.query.get(cpf)
        jg = Jogadas.query.get(cpf)
        cost = current_app.config['COST_PER_PLAY']

        # valida recursos
        if jg.jogadas <= 0 or pts.pontos < cost:
            return None, None, 'Sem recursos.'

        # debita custo da jogada (será registrado se perder sinos)
        pts.pontos -= cost
        jg.jogadas -= 1

        # sorteia 3 figuras
        results = [random.choice(FIGURES) for _ in range(3)]

        # conta ocorrências
        count_map = {f: results.count(f) for f in FIGURES}

        # determina recompensa ou penalidade
        # diamond = 50 por unidade, bell = -50 por unidade, crown jackpot = +1000
        diamond_count = count_map['3']  # supondo '3' representa diamond
        bell_count = count_map['7']  # supondo '7' representa bell
        crown_count = count_map['6']  # supondo '6' representa crown

        if crown_count == 3:
            net = 1000
        else:
            net = diamond_count * 50 - bell_count * 50

        # aplica variação net
        pts.pontos += net

        # prepara registro
        outcome = 'ganhou' if net > 0 else 'perder'
        registro = RegistroJogada(
            cpf=cpf,
            timestamp=datetime.utcnow(),
            resultado=outcome,
            quantidade=net  # positivo ou negativo conforme net
        )
        db.session.add(registro)

        # persiste tudo
        db.session.commit()
        return results, net, None

import random
from app.models import Pontos, Jogadas
from app.extensions import db
from flask import current_app

FIGURES = ['1','2','3','4','5','6','7']

class GameService:
    @staticmethod
    def spin(cpf):
        pts = Pontos.query.get(cpf)
        jg  = Jogadas.query.get(cpf)
        cost = current_app.config['COST_PER_PLAY']

        # valida recursos
        if jg.jogadas <= 0 or pts.pontos < cost:
            return None, None, 'Sem recursos.'

        # debita custo
        pts.pontos -= cost
        jg.jogadas -= 1

        # sorteia
        results = [random.choice(FIGURES) for _ in range(3)]
        hits = results.count('3')
        reward_map = {1:50, 2:100, 3:150}
        reward = reward_map.get(hits, 0)

        # dá recompensa
        pts.pontos += reward

        # persiste TUDO
        db.session.commit()

        return results, reward, None

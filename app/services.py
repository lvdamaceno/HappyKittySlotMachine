import random
from flask import current_app
from app.extensions import db
from app.models import PointTransaction

FIGURES = ['1','2','3','4','5','6','7']

class GameService:
    @staticmethod
    def spin(user):
        cost = current_app.config.get('COST_PER_PLAY', 100)
        user.coins -= cost
        user.attempts -= 1

        results = [random.choice(FIGURES) for _ in range(3)]
        count3 = results.count('3')
        reward_map = {1:50, 2:100, 3:150}
        reward = reward_map.get(count3, 0)
        user.coins += reward

        db.session.add(PointTransaction(user_id=user.id, change=-cost))
        if reward:
            db.session.add(PointTransaction(user_id=user.id, change=reward))
        db.session.commit()

        return results, reward
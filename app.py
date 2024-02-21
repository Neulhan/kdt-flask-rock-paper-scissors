from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy(app)


class RockPaperScissorsGameHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_choice = db.Column(db.String, nullable=False)
    computer_choice = db.Column(db.String, nullable=False)
    result = db.Column(db.String, nullable=False)


with app.app_context():
    db.create_all()


CHOICE_LIST = ["✌️", "✊", "✋"]


@app.route('/', methods=['GET', 'POST'])
def rock_paper_scissors_game():
    """가위 바위 보 게임 입니다."""
    message = ""

    if request.method == 'POST':
        user_choice = request.form.get("user")
        computer_choice = random.choice(CHOICE_LIST)

        if user_choice not in CHOICE_LIST:
            """제대로 된 요청이 아닌 경우"""
            message = "Not a valid choice"

        elif user_choice == computer_choice:
            """비긴 경우"""
            history = RockPaperScissorsGameHistory(user_choice=user_choice, computer_choice=computer_choice,
                                                   result="비겼습니다")
            db.session.add(history)
            db.session.commit()
            message = f"사용자 : {user_choice} 컴퓨터 : {computer_choice} 비겼습니다."
        elif (
                (user_choice == "✌️" and computer_choice == "✋") or
                (user_choice == "✊" and computer_choice == "✌️") or
                (user_choice == "✋" and computer_choice == "✊")
        ):
            """이긴 경우"""
            history = RockPaperScissorsGameHistory(user_choice=user_choice, computer_choice=computer_choice,
                                                   result="이겼습니다")
            db.session.add(history)
            db.session.commit()
            message = f"사용자 : {user_choice} 컴퓨터 : {computer_choice} 이겼습니다."
        else:
            """진 경우"""
            history = RockPaperScissorsGameHistory(user_choice=user_choice, computer_choice=computer_choice,
                                                   result="졌습니다")
            db.session.add(history)
            db.session.commit()
            message = f"사용자 : {user_choice} 컴퓨터 : {computer_choice} 졌습니다."

    histories = RockPaperScissorsGameHistory.query.all()
    win = RockPaperScissorsGameHistory.query.filter_by(result="이겼습니다").count()
    draw = RockPaperScissorsGameHistory.query.filter_by(result="비겼습니다").count()
    lose = RockPaperScissorsGameHistory.query.filter_by(result="졌습니다").count()

    context = {
        "message": message,
        "histories": histories,
        "win": win,
        "draw": draw,
        "lose": lose
    }

    return render_template("rock_paper_scissors_game.html", context=context)


if __name__ == '__main__':
    app.run(debug=True)

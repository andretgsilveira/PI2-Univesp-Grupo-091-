from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime

from werkzeug.utils import redirect

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://yqiuysyngegqzn:068cfd3a2f749b8c09fb2bcfc6e7739a3ab9cd9b69f7c0cdb8617d74770e86c7@ec2-44-197-128-108.compute-1.amazonaws.com:5432/ddlmbptv8chm8o'

    db = SQLAlchemy(app)

    class Images(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        path = db.Column(db.String(500))
        alt = db.Column(db.String(500))
        date_created = db.Column(db.DateTime, default=datetime.utcnow)

        def __repr__(self):
            return '<ID %r>' %self.id

    @app.route('/testeDB')
    def testDB():
        return "Hey!"

    @app.route('/manage')
    def manage():
        evaluations = Rating.query.order_by(Rating.date_created)
        return render_template('manage.html', evaluations=evaluations)

    @app.route('/delete/<int:id>')
    def delete(id):
        commentDelete = Rating.query.get_or_404(id)
        
        try:
            db.session.delete(commentDelete)
            db.session.commit()
            return redirect('/manage')
        except:
            return "Não foi possivel deletar o comentario"

    @app.route('/contato')
    def contato():
        return render_template('contato.html')

    @app.route('/')
    def index():
        ratingAvg = db.session.query(func.avg(Rating.star)).scalar()
        ratingLength = db.session.query(func.max(Rating.id)).scalar()
        evaluations = Rating.query.order_by(Rating.date_created)
        return render_template('index.html', evaluations=evaluations, ratingLength=ratingLength, ratingAvg=ratingAvg)

    @app.route('/rating', methods=["POST", "GET"])
    def rating():
        if request.method == "POST":                
            star_rating = request.form.get("rating")
            comment = request.form.get("comment")
            new_rating = Rating(star = star_rating, evaluation = comment )
        
            try:
                db.session.add(new_rating)
                db.session.commit()

                return redirect('/')
            except:
                return "Erro ao adicionar ao banco de dados"
        else:
            return redirect('/')

    return app
# Retire o comentario para testar via Pycharm
# test = create_app()
# test.run()
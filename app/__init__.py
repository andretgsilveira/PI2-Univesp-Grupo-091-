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
        __tablename__ = 'tb_images'
        id = db.Column(db.Integer, primary_key=True)
        path = db.Column(db.String(500))
        alt = db.Column(db.String(500))
        date_created = db.Column(db.DateTime, default=datetime.utcnow)

        def __repr__(self):
            return '<ID %r>' %self.id

    @app.route('/submit', methods=["POST"])
    def testDB():
        if request.method == 'POST':
            alt = request.form['descricao']

            new_image = Images(path = "teste", alt = alt)
            
            try:
                db.session.add(new_image)
                db.session.commit()

                return redirect('/')
            except:
                return f"Erro ao adicionar ao banco de dados {alt}"
        else:
            return redirect('/')

    @app.route('/cadastro')
    def manage():
        return  render_template('cadastro.html')

    @app.route('/delete/<int:id>')
    def delete(id):
        pass
        return

    @app.route('/contato')
    def contato():
        return render_template('contato.html')

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/rating', methods=["POST", "GET"])
    def rating():
        pass
        return redirect('/')

    return app

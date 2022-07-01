from flask import Flask, jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import cloudinary
import cloudinary.uploader
import os

DIRETORIO = 'C:\\Users\\andre\\Desktop\\PI2-Univesp-Grupo-091-\\static\\imagens\\Photos-001'
DIRETORIO_RELATIVO = '..\static\imagens\Photos-001'

app = Flask(__name__)

cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
    api_secret=os.getenv('API_SECRET'))

ENV = 'prod'
print( os.environ.get('DATABASE_URL', ''))

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Imagens(db.Model):
    __tablename__ = 'tb_imagens'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(500))
    relative_path = db.Column(db.String(500))
    descricao = db.Column(db.String(500))
    nome_do_arquivo = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<ID %r>' %self.id

    def __init__(self, path, descricao, nome_do_arquivo, relative_path):
        self.path = path
        self.relative_path = relative_path
        self.descricao = descricao
        self.nome_do_arquivo = nome_do_arquivo

#-----Criar db------
#db.create_all()
#-------------------

@app.route('/')
def index():
    imagens = Imagens.query.all() 
    return render_template('index.html', imagens = imagens)

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/cadastro')
def manage():
    imagens = Imagens.query.all()  
    return  render_template('cadastro.html', imagens = imagens)


'-----------CRUD----------------'


@app.route('/arquivos', methods=['GET'])
def lista_imagens():
    imagens = []
    for nome_do_arquivo in os.listdir(DIRETORIO):
        endereco_do_arquivo = os.path.join(DIRETORIO, nome_do_arquivo)
        if(os.path.isfile(endereco_do_arquivo)):
            imagens.append(nome_do_arquivo)
    return jsonify(imagens)

@app.route('/arquivos', methods=['POST'])
def post_imagem():

    cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
        api_secret=os.getenv('API_SECRET'))
    upload_result = None

    if request.method == 'POST':

        imagem = request.files['imagem']
        alt = request.form['descricao']
        nome_do_arquivo = imagem.filename
        tipo = imagem.mimetype

        if ENV == 'dev':
            caminho = os.path.join(DIRETORIO,  nome_do_arquivo)
            caminho_relativo = os.path.join(DIRETORIO_RELATIVO,  nome_do_arquivo)

            for nome_da_imagem_no_diretorio in os.listdir(DIRETORIO):
                if nome_da_imagem_no_diretorio == nome_do_arquivo:
                    return render_template('cadastro.html', message='Arquivo igual ou com mesmo nome, verifique e tente novamente!')

            imagem.save(os.path.join(DIRETORIO, nome_do_arquivo))
        else:
            upload_result = cloudinary.uploader.upload(imagem)
            app.logger.info(upload_result)
            caminho = upload_result['url']
            caminho_relativo = upload_result['url']

        
        if tipo == 'image/png' or tipo == 'image/jpeg':
  
            new_image = Imagens(path = caminho, relative_path = caminho_relativo, descricao= alt, nome_do_arquivo= nome_do_arquivo)
            
            try:
                db.session.add(new_image)
                db.session.commit()
                return render_template('cadastro.html', message='Arquivo enviado com sucesso!')
            except:
                return render_template('cadastro.html', message='Falha ao cadastrar o arquivo no DB!')
        else:
            return render_template('cadastro.html', message='Tipo de arquivo incorreto, selecione uma imagem png ou jpeg!', tipo=imagem.mimetype)


@app.route('/delete/<int:id>')
def delete(id):
    imagemDelete = Imagens.query.get_or_404(id)


    if ENV == 'dev':
        if os.path.exists(imagemDelete.path):
            os.remove(imagemDelete.path)
        else:
            print("The file does not exist")
            return redirect('/cadastro')
    else:
        pass
        '''----Em desenvolvimento. Necessario remover o nome do arquivo que esta ao final do caminho
            para repasar para api do cloudinary----'''
        #cloudinary.uploader.destroy(imagemDelete)

    '''------db-------'''
    try:
        db.session.delete(imagemDelete)
        db.session.commit()
        return redirect('/cadastro')
    except:
        return "Não foi possivel deletar a imagem"


if __name__ == '__main__':
    app.run()
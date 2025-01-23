from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

# configurações
app = Flask(__name__)

# essa chave secreta serve pra proteger dados guardados na sessão do navegador
# ela pode ser qualquer coisa, escolhi essa pq é engraçado
# EU AINDA VOU ESCONDER ELA, DEIXAR EM VARIÁVEIS DE AMBIENTE
# como ela não significa nada e ainda será definida por enquanto tá blz
app.secret_key = "meumicomacaco"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/wifisensing'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# criando uma tabela pra testar
class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(80), nullable = False)
    senha = db.Column(db.String(16), nullable = False)


# normal
@app.route("/", methods=['GET', 'POST'])
def login():
    db.create_all()

    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        if not senha or not email:
            # depois eu te falo sobre esse flash, ele é tipo o alert do javascript mas tem que mexer mt no html
            flash("Preencha todos os campos", 'error')
            return redirect("/")

        try:
            novo_usuario = Usuario( email = email, senha = senha)
            db.session.add(novo_usuario)
            db.session.commit()
            flash("Dados do usuário pegos com sucesso (eu sei que é um login mas se fosse um cadastro tava blz já)")
        
        except Exception as e:
            db.session.rollback()
            flash(f"Erro pra cadastrar: {e}", 'error')


    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)


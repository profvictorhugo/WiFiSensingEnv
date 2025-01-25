from config import db

class Usuario(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(120), unique=True, nullable=False)
        senha = db.Column(db.String(16), nullable=False)


        def to_Json(self):
                return {
                        "id": self.id,
                        "email": self.email,
                        "senha": self.senha
                }


class Dispositivo(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        nome = db.Column(db.String(90))
        descricao = db.Column(db.String(150))
        script_configuracao = db.Column(db.String(200))


        def to_Json(self):
                return {
                        "id": self.id,
                        "nome": self.nome,
                        "descrição": self.descricao,
                        "script_configuração": self.script_configuracao
                }




from config import db

class Usuario(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(120), unique=True, nullable=False)
        senha = db.Column(db.String(16), nullable=False)


        def __init__(self, email, senha):
                self.email = email,
                self.senha = senha


        def to_Json(self):
                return {
                        "id": self.id,
                        "email": self.email,
                        "senha": self.senha
                }



class Dispositivo(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        codigo = db.Column(db.String(9), unique = True)
        nome = db.Column(db.String(90))
        descricao = db.Column(db.String(150))
        script_configuracao = db.Column(db.String(200))


        def __init__(self, codigo, nome, descricao, script):
                self.codigo = codigo,
                self.nome = nome,
                self.descricao = descricao,
                self.script_configuracao = script


        def to_Json(self):
                return {
                        "id": self.id,
                        "codigo": self.codigo,
                        "nome": self.nome,
                        "descrição": self.descricao,
                        "script_configuração": self.script_configuracao
                }


class Dataset(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        url = db.Column(db.String(120), nullable = False, unique = True)
        nome = db.Column(db.String(90))
        descricao = db.Column(db.String(150))


        def __init__(self, id, url, nome, desc):
                self.id = id
                self.url = url
                self.nome = nome
                self.descricao = desc


        def to_Json(self):
                return {
                        "id": self.id,
                        "url": self.url,
                        "nome": self.nome,
                        "descrição": self.descricao
                }

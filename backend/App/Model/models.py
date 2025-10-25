from app.config import db

class Usuario(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(120), unique=True, nullable=False)
        senha = db.Column(db.String(16), nullable=False)

        modelos = db.relationship("Modelo", backref = "usuario", cascade = "all, delete") # se eu tirar o usuário, seus modelos tbm vão embora do bd, deixar assim por enquanto


        def __init__(self, email, senha):
                self.email = email
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
                self.codigo = codigo
                self.nome = nome
                self.descricao = descricao
                self.script_configuracao = script


        def to_Json(self):
                return {
                        "id": self.id,
                        "codigo": self.codigo,
                        "nome": self.nome,
                        "descricao": self.descricao,
                        "script_configuracao": self.script_configuracao
                }


class Dataset(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        url = db.Column(db.String(120), nullable = False, unique = True)
        nome = db.Column(db.String(90))
        descricao = db.Column(db.String(150))


        def __init__(self, url, nome, desc):
                self.url = url
                self.nome = nome
                self.descricao = desc


        def to_Json(self):
                return {
                        "id": self.id,
                        "url": self.url,
                        "nome": self.nome,
                        "descricao": self.descricao
                }


class Modelo(db.Model):
        id = db.Column(db.Integer, primary_key = True)

        id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id", ondelete="CASCADE"))
        
        url = db.Column(db.String(120), nullable = False, unique = True)
        nome = db.Column(db.String(90))
        descricao = db.Column(db.String(150))


        def __init__(self, id_usuario, url, nome, descricao):
                self.id_usuario = id_usuario
                self.url = url
                self.nome = nome
                self.descricao = descricao


        def to_Json(self):
                return {
                        "url": self.url,
                        "id_usuario": self.id_usuario,
                        "nome": self.nome,
                        "descricao": self.descricao
                }


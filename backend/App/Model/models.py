import base64

from App.Configuration.config import db

class Usuario(db.Model):
        id      = db.Column(db.Integer, primary_key=True)
        email   = db.Column(db.String(120), unique=True, nullable=False)
        senha   = db.Column(db.String(16), nullable=False)
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
        id        = db.Column(db.Integer, primary_key = True)
        codigo    = db.Column(db.String(9), unique = True)
        nome      = db.Column(db.String(90))
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
        id        = db.Column(db.Integer, primary_key = True)
        url       = db.Column(db.String(120), nullable = False, unique = True)
        nome      = db.Column(db.String(90))
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
        id = db.Column(db.Integer, primary_key=True)
        id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id", ondelete="CASCADE"))

        tipo = db.Column(db.Enum("IA", "Sistema", name="modelo_tipo"), nullable=False, default="IA")

        # Se o modelo estiver salvo no PC, use `url`.
        # Se estiver salvo no banco, use `modelo` (blob) e deixe `url` nulo.
        url = db.Column(db.String(120), nullable=True, unique=True)
        modelo = db.Column(db.LargeBinary, nullable=True)

        nome = db.Column(db.String(90))
        descricao = db.Column(db.String(150))

        descricao_algoritmo = db.Column(db.Text, nullable=True)
        parametros = db.Column(db.JSON, nullable=True)

        # "Fontes de dados" para um Sistema: filhos da própria tabela Modelo
        id_pai = db.Column(db.Integer, db.ForeignKey("modelo.id", ondelete="CASCADE"), nullable=True)
        fontes_dados = db.relationship(
            "Modelo",
            cascade="all, delete",
            backref=db.backref("pai", remote_side=[id]),
            passive_deletes=True,
        )

        itens_modelo = db.relationship(
            "ItemModelo",
            cascade="all, delete-orphan",
            backref="modelo_pai",
            passive_deletes=True,
        )

        def __init__(
            self,
            id_usuario,
            tipo="IA",
            url=None,
            modelo=None,
            nome=None,
            descricao=None,
            descricao_algoritmo=None,
            parametros=None,
            id_pai=None,
        ):
            self.id_usuario = id_usuario
            self.tipo = tipo
            self.url = url
            self.modelo = modelo
            self.nome = nome
            self.descricao = descricao
            self.descricao_algoritmo = descricao_algoritmo
            self.parametros = parametros
            self.id_pai = id_pai

        def to_Json(self, include_modelo=False):
            json_data = {
                "id": self.id,
                "id_usuario": self.id_usuario,
                "tipo": self.tipo,
                "url": self.url,
                "tem_modelo_no_banco": bool(self.modelo),
                "nome": self.nome,
                "descricao": self.descricao,
                "descricao_algoritmo": self.descricao_algoritmo,
                "parametros": self.parametros,
                "id_pai": self.id_pai,
                "fontes_dados": [{"id": m.id, "url": m.url, "tipo": m.tipo, "nome": m.nome} for m in (self.fontes_dados or [])],
                "itens_modelo": [item.to_Json() for item in (self.itens_modelo or [])],
            }

            if include_modelo and self.modelo is not None:
                json_data["modelo"] = base64.b64encode(self.modelo).decode("utf-8")

            return json_data


class ItemModelo(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        id_pai = db.Column(db.Integer, db.ForeignKey("modelo.id", ondelete="CASCADE"), nullable=False)
        nome = db.Column(db.String(90), nullable=False)
        descricao = db.Column(db.String(300), nullable=True)

        def __init__(self, id_pai, nome, descricao=None):
            self.id_pai = id_pai
            self.nome = nome
            self.descricao = descricao

        def to_Json(self):
            return {
                "id": self.id,
                "id_pai": self.id_pai,
                "nome": self.nome,
                "descricao": self.descricao,
            }

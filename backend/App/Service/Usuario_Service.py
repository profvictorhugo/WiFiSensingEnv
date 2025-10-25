from App.config import db
from App.Model.models import Usuario

class UsuarioService:

    @staticmethod
    def login_usuario(email: str, senha: str):

        if not email or not senha:
            return {"mensagem": "informe o email e a senha"}, 400

        usuario = Usuario.query.filter(Usuario.email == email, Usuario.senha == senha).first()
        if not usuario:
            return {"mensagem": "nenhum usuáario encontrado"}, 404

        return {"mensagem": "logado"}, 200


    @staticmethod
    def cadastrar_usuario(email: str, senha: str):

        if not email or not senha:
            return {"mensagem": "preencha o email e a senha"}, 400

        novo_usuario = Usuario(email=email, senha=senha)

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            return {"mensagem": "Usuário criado"}, 201

        except Exception as e:
            db.session.rollback()
            return {"erro": f"não foi possível cadastrar usuário :: {str(e)}"}, 400



    @staticmethod
    def consulta_usuario(email: str):

        if not email:
            return {"mensagem": "nenhum email passado"}, 400

        usuario = Usuario.query.filter(Usuario.email == email).first()

        if not usuario:
            return {"mensagem": "nenhum usuário encontrado"}, 400

        json_usuario = usuario.to_Json()
        return {"usuáro encontrado": json_usuario}, 201


    @staticmethod
    def altera_usuario(email: str, nova_senha: str):

        if not email:
            return {"mensagem": "informe o email"}, 400

        if not nova_senha:
                return {"mensagem": "nenhuma senha passada"}, 401

        usuario = Usuario.query.filter(Usuario.email == email).first()
        if not usuario:
                return {"mensagem": "ninguém encontrado com esse email"}, 404

        try:
            usuario.senha = nova_senha
            db.session.commit()
            return {"mensagem": "senha alterada"}, 200

        except Exception as e:
            db.session.rollback()
            return {"erro", f"erro ao alterar senha :: {str(e)}"}, 400


    @staticmethod
    def remove_usuario(email: str):

        if not email:
            return {"mensagem": "informe o email"}, 400

        usuario = Usuario.query.filter(Usuario.email == email).first()
        if not usuario:
            return {"mensagem": "usuário não encontrado"}, 404

        try:
            db.session.delete(usuario)
            db.session.commit()
            return {"mensagem": "usuário removido"}, 200

        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"não foi possível tirar do banco de dados :: {str(e)}"}, 400


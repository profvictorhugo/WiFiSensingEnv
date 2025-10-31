from App.Model.models import db
from App.Model.models import Usuario, Modelo

class ModeloService:

    @staticmethod
    def cadastra(email: str, url: str, nome: str, descricao: str):

        if not email or not url:
            return {"mensagem": "informe os campos necessários"}, 400

        usuario = Usuario.query.filter(Usuario.email == email).first()
        if not usuario:
            return {"mensagem": "esse email não está cadastrado"}, 403


        modelo = Modelo(
            id_usuario = usuario.id,
            url        = url,
            nome       = nome,
            descricao  = descricao
        )

        try:
            db.session.add(modelo)
            db.session.commit()
            return {"mensagem": "modelo cadastrado com sucesso"}, 200

        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"não foi possível cadastrar :: {str(e)}"}, 400


    @staticmethod
    def consulta(url: str):

        if not url:
            return {"mensagem": "informe a url do modelo"}, 400

        modelo = Modelo.query.filter(Modelo.url == url).first()
        if not modelo:
            return {"mensagem": "nenhum modelo encontrado com essa url"}, 403

        json_modelo = modelo.to_Json()
        return {"mensagem": f"modelo: {json_modelo}"}, 200


    @staticmethod
    def consulta_todos():

        modelos = Modelo.query.all()

        modelos_json = [modelo.to_Json() for modelo in modelos]

        return {"modelos": modelos_json}, 200


    @staticmethod
    def altera(url: str, nova_url: str, novo_nome: str, nova_desc: str):

        if not url:
            return {"mensagem": "informe a url do modelo que deseja alterar"}, 400

        modelo = Modelo.query.filter(Modelo.url == url).first()
        if not modelo:
            return {"mensagem": "modelo não encontrado"}, 403


        if nova_url:
            modelo.url = nova_url

        if novo_nome:
            modelo.nome = novo_nome

        if nova_desc:
            modelo.descricao = nova_desc


        try:
            db.session.commit()
            return {"mensagem": "alterações salvas"}, 200

        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"não foi possível submeter as mudanças :: {str(e)}"}, 400


    @staticmethod
    def remove(url: str):

        if not url:
            return {"mensagem": "informe o url do modelo"}, 400

        modelo = Modelo.query.filter(Modelo.url == url).first()
        if not modelo:
            return {"mensagem": "nenhum modelo com essa url encontrado"}, 403

        try:
            db.session.delete(modelo)
            db.session.commit()
            return {"mensagem": "modelo deletado"}, 200

        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"não foi possível deletar o modelo :: {str(e)}"}, 400


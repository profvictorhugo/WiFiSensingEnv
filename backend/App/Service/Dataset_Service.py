from App.config import db
from App.Model.models import Dataset

class DatasetService:

    @staticmethod
    def cadastra(url: str, nome: str, desc: str):

        if not url or not nome or not desc:
            return {"mensagem": "informe a url"}, 400

        dataset = Dataset(
            url  = url,
            nome = nome,
            desc = desc
        )

        try:
            db.session.add(dataset)
            db.session.commit()
            return {"mensagem": "dataset cadastrado"}, 200

        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"erro na criação no banco de dados :: {str(e)}"}, 400


    @staticmethod
    def consulta(url: str):

        if not url:
            return {"mensagem": "informe a url do dataset"}, 400

        dataset = Dataset.query.filter(Dataset.url == url).first()
        if not dataset:
            return {"mensagem": "nenhum dataset encontrado"}, 403

        return {"mensagem": "dataset encontrado"}, 200


    @staticmethod
    def altera(url: str, nome: str, desc: str):

        if not url:
            return {"mensagem": "informe o url"}, 400

        dataset = Dataset.query.filter(Dataset.url == url).first()
        if not dataset:
            return {"mensagem": "nenhum dataset encontrado"}, 403

        novo_nome = nome
        nova_desc = desc

        if novo_nome:
            dataset.nome = novo_nome

        if nova_desc:
            dataset.descricao = nova_desc

        try:
            db.session.commit()
            return {"mensagem": "dataset alterado"}, 200

        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"erro ao alterar dados no banco de dados :: {str(e)}"}, 400


    @staticmethod
    def remove(url: str):

        if not url:
            return {"mensagem": "informe o url"}, 400

        dataset = Dataset.query.filter(Dataset.url == url).first()
        if not dataset:
            return {"mensagem": "nenhum dataset encontrado"}, 403

        try:
            db.session.delete(dataset)
            db.session.commit()
            return {"mensagem": "dataset deletado"}, 200

        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"não foi possível deletar do banco de dados :: {str(e)}"}, 400









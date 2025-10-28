from App.config import db
from App.Model.models import Dispositivo

class DispositivoService:

    @staticmethod
    def cadastra(nome: str, descricao: str, codigo: str ,script: str):

        if not codigo or not nome or not codigo or not descricao or not script:
            return {"mensagem": "informe os campos necessários para criação"}, 400

        novo_dispositivo = Dispositivo(
            nome      = nome,
            codigo    = codigo,
            descricao = descricao,
            script    = script
        )

        try:
            db.session.add(novo_dispositivo)
            db.session.commit()
            return {"mensagem": "dispositivo cadastrado"}, 201

        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"erro ao cadastrar no banco de dados :: {str(e)}"}, 400


    @staticmethod
    def altera(codigo: str, nome: str, descricao: str, script: str):

        if not codigo:
            return {"mensagem": "informe o código do dispositivo"}, 400

        dispositivo = Dispositivo.query.filter(Dispositivo.codigo == codigo).first()
        if not dispositivo:
            return {"mensagem": "esse código não consta no banco de dados"}, 403


        if nome:
            dispositivo.nome = nome

        if descricao:
            dispositivo.descricao = descricao

        if script:
            dispositivo.script_configuracao = script


        try:
            db.session.commit()
            return {"mensagem": "dados alterados"}, 200

        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"erro ao alterar no banco de dados :: {str(e)}"}, 400


    @staticmethod
    def remove(codigo: str):

        if not codigo:
            return {"mensagem": "nenhum código informado"}, 400

        disp = Dispositivo.query.filter(Dispositivo.codigo == codigo).first()
        if not disp:
            return {"mensagem": "dispositivo não encontrado"}, 403

        try:
            db.session.delete(disp)
            db.session.commit()
            return {"mensagem": "dispositivo removido"}, 200

        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"erro ao deletar do banco de dados :: {str(e)}"}, 400


    @staticmethod
    def consulta(codigo: str):

        if not codigo:
                return {"mensagem": "nenhum código passado"}, 400

        disp = Dispositivo.query.filter(Dispositivo.codigo == codigo).first()
        if not disp:
                return {"mensagem": "nenhum dispositivo encontrado"}, 403

        json_disp = disp.to_Json()

        return {"dispositivo": json_disp}, 200


    @staticmethod
    def consulta_todos():

        dispositivos = Dispositivo.query.all()

        disp_json = [disp.to_Json() for disp in dispositivos]

        return {"dispositivos": disp_json}, 200
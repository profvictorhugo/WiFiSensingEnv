import base64

from App.Configuration.config import db
from App.Model.models import ItemModelo, Modelo, Usuario


class ModeloService:

    @staticmethod
    def _decode_modelo_base64(modelo_base64):
        if modelo_base64 is None:
            return None, None

        if not isinstance(modelo_base64, str) or modelo_base64.strip() == "":
            return None, {"mensagem": "campo 'modelo' deve ser base64 (string)"}

        try:
            return base64.b64decode(modelo_base64), None
        except Exception:
            return None, {"mensagem": "campo 'modelo' inválido (base64)"}

    @staticmethod
    def _normaliza_tipo(tipo):
        if not tipo:
            return "IA"
        if not isinstance(tipo, str):
            return None

        tipo_raw = tipo.strip()
        tipo_upper = tipo_raw.upper()
        if tipo_upper == "IA":
            return "IA"
        if tipo_upper == "SISTEMA":
            return "Sistema"

        if tipo_raw in ["IA", "Sistema"]:
            return tipo_raw

        return None

    @staticmethod
    def _valida_url_x_modelo(tipo, url, modelo_bytes, modelo_base64_enviado):
        if url and modelo_base64_enviado:
            return {"mensagem": "preencha apenas um: 'url' (PC) ou 'modelo' (banco)"}

        if tipo == "IA":
            if not url and modelo_bytes is None:
                return {"mensagem": "para tipo IA informe 'url' ou 'modelo' (base64)"}

        return None

    @staticmethod
    def _upsert_itens_modelo(modelo: Modelo, itens_modelo):
        if itens_modelo is None:
            return None

        if not isinstance(itens_modelo, list):
            return {"mensagem": "itens_modelo deve ser uma lista"}

        for item in list(modelo.itens_modelo or []):
            db.session.delete(item)

        for item in itens_modelo:
            if not isinstance(item, dict):
                return {"mensagem": "cada item de itens_modelo deve ser um objeto {nome, descricao}"}

            nome = item.get("nome")
            descricao = item.get("descricao") or item.get("desc")

            if not nome or str(nome).strip() == "":
                return {"mensagem": "itens_modelo[].nome é obrigatório"}

            db.session.add(ItemModelo(id_pai=modelo.id, nome=nome, descricao=descricao))

        return None

    @staticmethod
    def _upsert_fontes_dados(modelo: Modelo, fontes_dados):
        if fontes_dados is None:
            return None

        if not isinstance(fontes_dados, list):
            return {"mensagem": "fontes_dados deve ser uma lista (urls ou objetos)"}

        # Desassocia todos os filhos atuais.
        for filho in list(modelo.fontes_dados or []):
            filho.id_pai = None

        for fd in fontes_dados:
            if isinstance(fd, str):
                url = fd.strip()
                if url == "":
                    continue

                filho = Modelo.query.filter(Modelo.url == url).first()
                if not filho:
                    return {"mensagem": f"fonte de dados não encontrada: {url}"}

                filho.id_pai = modelo.id
                continue

            if isinstance(fd, dict):
                tipo_fd = ModeloService._normaliza_tipo(fd.get("tipo") or "IA")
                if not tipo_fd:
                    return {"mensagem": "tipo inválido em fontes_dados"}

                url = fd.get("url")
                nome = fd.get("nome")
                descricao = fd.get("descricao")
                descricao_algoritmo = fd.get("descricao_algoritmo")
                parametros = fd.get("parametros")
                if parametros is None:
                    parametros = fd.get("parâmetros")
                modelo_base64 = fd.get("modelo")

                modelo_bytes, err = ModeloService._decode_modelo_base64(modelo_base64)
                if err:
                    return err

                err = ModeloService._valida_url_x_modelo(tipo_fd, url, modelo_bytes, modelo_base64 is not None)
                if err:
                    return err

                filho = Modelo(
                    id_usuario=modelo.id_usuario,
                    tipo=tipo_fd,
                    url=url if url else None,
                    modelo=modelo_bytes,
                    nome=nome,
                    descricao=descricao,
                    descricao_algoritmo=descricao_algoritmo,
                    parametros=parametros,
                    id_pai=modelo.id,
                )
                db.session.add(filho)
                continue

            return {"mensagem": "fontes_dados deve conter strings (urls) ou objetos"}

        return None

    @staticmethod
    def cadastra(
        email: str,
        tipo: str = None,
        url: str = None,
        nome: str = None,
        descricao: str = None,
        descricao_algoritmo: str = None,
        parametros=None,
        modelo_base64: str = None,
        id_pai: int = None,
        fontes_dados=None,
        itens_modelo=None,
    ):
        if not email:
            return {"mensagem": "informe o email"}, 400

        usuario = Usuario.query.filter(Usuario.email == email).first()
        if not usuario:
            return {"mensagem": "esse email não está cadastrado"}, 403

        tipo_norm = ModeloService._normaliza_tipo(tipo)
        if not tipo_norm:
            return {"mensagem": "tipo inválido (use 'IA' ou 'Sistema')"}, 400

        modelo_bytes, err = ModeloService._decode_modelo_base64(modelo_base64)
        if err:
            return err, 400

        err = ModeloService._valida_url_x_modelo(tipo_norm, url, modelo_bytes, modelo_base64 is not None)
        if err:
            return err, 400

        novo_modelo = Modelo(
            id_usuario=usuario.id,
            tipo=tipo_norm,
            url=url if url else None,
            modelo=modelo_bytes,
            nome=nome,
            descricao=descricao,
            descricao_algoritmo=descricao_algoritmo,
            parametros=parametros,
            id_pai=id_pai,
        )

        try:
            db.session.add(novo_modelo)
            db.session.flush()  # garante `id` para relacionamentos

            if tipo_norm == "Sistema":
                err = ModeloService._upsert_itens_modelo(novo_modelo, itens_modelo)
                if err:
                    db.session.rollback()
                    return err, 400

                err = ModeloService._upsert_fontes_dados(novo_modelo, fontes_dados)
                if err:
                    db.session.rollback()
                    return err, 400

            db.session.commit()
            return {"mensagem": "modelo cadastrado com sucesso", "modelo": novo_modelo.to_Json(include_modelo=False)}, 200

        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"não foi possível cadastrar :: {str(e)}"}, 400

    @staticmethod
    def consulta_por_url(url: str):
        if not url:
            return {"mensagem": "informe a url do modelo"}, 400

        modelo = Modelo.query.filter(Modelo.url == url).first()
        if not modelo:
            return {"mensagem": "nenhum modelo encontrado com essa url"}, 404

        return {"modelo": modelo.to_Json(include_modelo=True)}, 200

    @staticmethod
    def consulta_por_id(id: int):
        if not id:
            return {"mensagem": "informe o id do modelo"}, 400

        modelo = Modelo.query.filter(Modelo.id == id).first()
        if not modelo:
            return {"mensagem": "nenhum modelo encontrado com esse id"}, 404

        return {"modelo": modelo.to_Json(include_modelo=True)}, 200

    @staticmethod
    def consulta_todos():
        modelos = Modelo.query.all()
        modelos_json = [modelo.to_Json(include_modelo=False) for modelo in modelos]
        return {"modelos": modelos_json}, 200

    @staticmethod
    def _altera_modelo_obj(
        modelo: Modelo,
        nova_url: str = None,
        novo_nome: str = None,
        nova_desc: str = None,
        descricao_algoritmo: str = None,
        parametros=None,
        modelo_base64: str = None,
        id_pai: int = None,
        fontes_dados=None,
        itens_modelo=None,
    ):
        if nova_url is not None and modelo_base64 is not None:
            return {"mensagem": "preencha apenas um: 'nova_url' ou 'modelo' (base64)"}

        if novo_nome is not None:
            modelo.nome = novo_nome

        if nova_desc is not None:
            modelo.descricao = nova_desc

        if descricao_algoritmo is not None:
            modelo.descricao_algoritmo = descricao_algoritmo

        if parametros is not None:
            modelo.parametros = parametros

        if id_pai is not None:
            modelo.id_pai = id_pai

        if nova_url is not None:
            modelo.url = nova_url if str(nova_url).strip() != "" else None
            if modelo.url is not None:
                modelo.modelo = None

        if modelo_base64 is not None:
            modelo_bytes, err = ModeloService._decode_modelo_base64(modelo_base64)
            if err:
                return err

            modelo.modelo = modelo_bytes
            modelo.url = None

        err = ModeloService._valida_url_x_modelo(modelo.tipo, modelo.url, modelo.modelo, modelo_base64 is not None)
        if err:
            return err

        if modelo.tipo == "Sistema":
            err = ModeloService._upsert_itens_modelo(modelo, itens_modelo)
            if err:
                return err

            err = ModeloService._upsert_fontes_dados(modelo, fontes_dados)
            if err:
                return err

        return None

    @staticmethod
    def altera_por_url(
        url: str,
        nova_url: str = None,
        novo_nome: str = None,
        nova_desc: str = None,
        descricao_algoritmo: str = None,
        parametros=None,
        modelo_base64: str = None,
        id_pai: int = None,
        fontes_dados=None,
        itens_modelo=None,
    ):
        if not url:
            return {"mensagem": "informe a url do modelo que deseja alterar"}, 400

        modelo = Modelo.query.filter(Modelo.url == url).first()
        if not modelo:
            return {"mensagem": "modelo não encontrado"}, 404

        err = ModeloService._altera_modelo_obj(
            modelo=modelo,
            nova_url=nova_url,
            novo_nome=novo_nome,
            nova_desc=nova_desc,
            descricao_algoritmo=descricao_algoritmo,
            parametros=parametros,
            modelo_base64=modelo_base64,
            id_pai=id_pai,
            fontes_dados=fontes_dados,
            itens_modelo=itens_modelo,
        )
        if err:
            return err, 400

        try:
            db.session.commit()
            return {"mensagem": "alterações salvas", "modelo": modelo.to_Json(include_modelo=False)}, 200
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"não foi possível submeter as mudanças :: {str(e)}"}, 400

    @staticmethod
    def altera_por_id(
        id: int,
        nova_url: str = None,
        novo_nome: str = None,
        nova_desc: str = None,
        descricao_algoritmo: str = None,
        parametros=None,
        modelo_base64: str = None,
        id_pai: int = None,
        fontes_dados=None,
        itens_modelo=None,
    ):
        if not id:
            return {"mensagem": "informe o id do modelo que deseja alterar"}, 400

        modelo = Modelo.query.filter(Modelo.id == id).first()
        if not modelo:
            return {"mensagem": "modelo não encontrado"}, 404

        err = ModeloService._altera_modelo_obj(
            modelo=modelo,
            nova_url=nova_url,
            novo_nome=novo_nome,
            nova_desc=nova_desc,
            descricao_algoritmo=descricao_algoritmo,
            parametros=parametros,
            modelo_base64=modelo_base64,
            id_pai=id_pai,
            fontes_dados=fontes_dados,
            itens_modelo=itens_modelo,
        )
        if err:
            return err, 400

        try:
            db.session.commit()
            return {"mensagem": "alterações salvas", "modelo": modelo.to_Json(include_modelo=False)}, 200
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"não foi possível submeter as mudanças :: {str(e)}"}, 400

    @staticmethod
    def remove_por_url(url: str):
        if not url:
            return {"mensagem": "informe o url do modelo"}, 400

        modelo = Modelo.query.filter(Modelo.url == url).first()
        if not modelo:
            return {"mensagem": "nenhum modelo com essa url encontrado"}, 404

        try:
            db.session.delete(modelo)
            db.session.commit()
            return {"mensagem": "modelo deletado"}, 200
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"não foi possível deletar o modelo :: {str(e)}"}, 400

    @staticmethod
    def remove_por_id(id: int):
        if not id:
            return {"mensagem": "informe o id do modelo"}, 400

        modelo = Modelo.query.filter(Modelo.id == id).first()
        if not modelo:
            return {"mensagem": "nenhum modelo com esse id encontrado"}, 404

        try:
            db.session.delete(modelo)
            db.session.commit()
            return {"mensagem": "modelo deletado"}, 200
        except Exception as e:
            db.session.rollback()
            return {"mensagem": f"não foi possível deletar o modelo :: {str(e)}"}, 400


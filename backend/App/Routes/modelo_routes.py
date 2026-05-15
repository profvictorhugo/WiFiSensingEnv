from flask import Blueprint, jsonify, request

from App.Service.Modelo_Service import ModeloService

modelo_bp = Blueprint("modelo_bp", __name__)


@modelo_bp.route("/modelos", methods=["POST"])
def cadastra_modelo():
    data = request.get_json(silent=True) or {}

    email = data.get("email")
    tipo = data.get("tipo")
    url = data.get("url")
    nome = data.get("nome")
    descricao = data.get("descricao")
    descricao_algoritmo = data.get("descricao_algoritmo") or data.get("descrição_do_algoritmo")

    parametros = data.get("parametros")
    if parametros is None:
        parametros = data.get("parâmetros")

    modelo_base64 = data.get("modelo")

    id_pai = data.get("id_pai")
    fontes_dados = data.get("fontes_dados")
    itens_modelo = data.get("itens_modelo") or data.get("itens")

    response, status = ModeloService.cadastra(
        email=email,
        tipo=tipo,
        url=url,
        nome=nome,
        descricao=descricao,
        descricao_algoritmo=descricao_algoritmo,
        parametros=parametros,
        modelo_base64=modelo_base64,
        id_pai=id_pai,
        fontes_dados=fontes_dados,
        itens_modelo=itens_modelo,
    )
    return jsonify(response), status


@modelo_bp.route("/modelos/<path:url>", methods=["GET"])
def consulta_modelo(url: str):
    response, status = ModeloService.consulta_por_url(url)
    return jsonify(response), status


@modelo_bp.route("/modelos/id/<int:id>", methods=["GET"])
def consulta_modelo_por_id(id: int):
    response, status = ModeloService.consulta_por_id(id)
    return jsonify(response), status


@modelo_bp.route("/modelos", methods=["GET"])
def consulta_modelos():
    response, status = ModeloService.consulta_todos()
    return jsonify(response), status


@modelo_bp.route("/modelos/<path:url>", methods=["PATCH"])
def altera_modelo(url: str):
    data = request.get_json(silent=True) or {}

    nova_url = data.get("nova_url")
    novo_nome = data.get("novo_nome")
    nova_descricao = data.get("nova_descricao")
    nova_descricao_algoritmo = data.get("descricao_algoritmo") or data.get("descrição_do_algoritmo")

    parametros = data.get("parametros")
    if parametros is None:
        parametros = data.get("parâmetros")

    modelo_base64 = data.get("modelo")
    novo_id_pai = data.get("id_pai")

    fontes_dados = data.get("fontes_dados")
    itens_modelo = data.get("itens_modelo") or data.get("itens")

    response, status = ModeloService.altera_por_url(
        url=url,
        nova_url=nova_url,
        novo_nome=novo_nome,
        nova_desc=nova_descricao,
        descricao_algoritmo=nova_descricao_algoritmo,
        parametros=parametros,
        modelo_base64=modelo_base64,
        id_pai=novo_id_pai,
        fontes_dados=fontes_dados,
        itens_modelo=itens_modelo,
    )
    return jsonify(response), status


@modelo_bp.route("/modelos/id/<int:id>", methods=["PATCH"])
def altera_modelo_por_id(id: int):
    data = request.get_json(silent=True) or {}

    nova_url = data.get("nova_url")
    novo_nome = data.get("novo_nome")
    nova_descricao = data.get("nova_descricao")
    nova_descricao_algoritmo = data.get("descricao_algoritmo") or data.get("descrição_do_algoritmo")

    parametros = data.get("parametros")
    if parametros is None:
        parametros = data.get("parâmetros")

    modelo_base64 = data.get("modelo")
    novo_id_pai = data.get("id_pai")

    fontes_dados = data.get("fontes_dados")
    itens_modelo = data.get("itens_modelo") or data.get("itens")

    response, status = ModeloService.altera_por_id(
        id=id,
        nova_url=nova_url,
        novo_nome=novo_nome,
        nova_desc=nova_descricao,
        descricao_algoritmo=nova_descricao_algoritmo,
        parametros=parametros,
        modelo_base64=modelo_base64,
        id_pai=novo_id_pai,
        fontes_dados=fontes_dados,
        itens_modelo=itens_modelo,
    )
    return jsonify(response), status


@modelo_bp.route("/modelos/<path:url>", methods=["DELETE"])
def remove_modelo(url: str):
    response, status = ModeloService.remove_por_url(url)
    return jsonify(response), status


@modelo_bp.route("/modelos/id/<int:id>", methods=["DELETE"])
def remove_modelo_por_id(id: int):
    response, status = ModeloService.remove_por_id(id)
    return jsonify(response), status


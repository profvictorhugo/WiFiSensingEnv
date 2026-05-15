from flask import Blueprint, jsonify, request

from App.Service.Dispositivo_Service import DispositivoService

dispositivo_bp = Blueprint("dispositivo_bp", __name__)


@dispositivo_bp.route("/dispositivos", methods=["POST"])
def cadastra_dispositivo():
    data = request.get_json(silent=True) or {}

    nome = data.get("nome")
    descricao = data.get("descricao")
    codigo = data.get("codigo")
    script = data.get("script")

    response, status = DispositivoService.cadastra(nome, descricao, codigo, script)
    return jsonify(response), status


@dispositivo_bp.route("/dispositivos/<codigo>", methods=["PATCH"])
def altera_dispositivo(codigo: str):
    data = request.get_json(silent=True) or {}

    nome = data.get("nome")
    descricao = data.get("descricao")
    script = data.get("script")

    response, status = DispositivoService.altera(codigo, nome, descricao, script)
    return jsonify(response), status


@dispositivo_bp.route("/dispositivos/<codigo>", methods=["DELETE"])
def remove_dispositivo(codigo: str):
    response, status = DispositivoService.remove(codigo)
    return jsonify(response), status


@dispositivo_bp.route("/dispositivos/<codigo>", methods=["GET"])
def consulta_dispositivo(codigo: str):
    response, status = DispositivoService.consulta(codigo)
    return jsonify(response), status


@dispositivo_bp.route("/dispositivos", methods=["GET"])
def consulta_dispositivos():
    response, status = DispositivoService.consulta_todos()
    return jsonify(response), status


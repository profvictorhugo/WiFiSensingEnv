from flask import Blueprint, jsonify, request

from App.Service.Usuario_Service import UsuarioService

usuario_bp = Blueprint("usuario_bp", __name__)


@usuario_bp.route("/login", methods=["POST"])
def logar_usuario():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    senha = data.get("senha")

    response, status = UsuarioService.login(email, senha)
    return jsonify(response), status


@usuario_bp.route("/usuarios", methods=["POST"])
def cadastra_usuario():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    senha = data.get("senha")

    response, status = UsuarioService.cadastra(email, senha)
    return jsonify(response), status


@usuario_bp.route("/usuarios/<int:id>", methods=["GET"])
def consulta_usuario(id: int):
    response, status = UsuarioService.consulta(id)
    return jsonify(response), status


@usuario_bp.route("/usuarios", methods=["GET"])
def consulta_usuarios():
    response, status = UsuarioService.consulta_todos()
    return jsonify(response), status


@usuario_bp.route("/usuarios/<int:id>", methods=["PATCH"])
def altera_usuario(id: int):
    data = request.get_json(silent=True) or {}
    nova_senha = data.get("nova_senha")

    response, status = UsuarioService.altera(id, nova_senha)
    return jsonify(response), status


@usuario_bp.route("/usuarios/<int:id>", methods=["DELETE"])
def remove_usuario(id: int):
    response, status = UsuarioService.remove(id)
    return jsonify(response), status


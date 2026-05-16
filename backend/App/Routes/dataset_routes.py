from flask import Blueprint, jsonify, request
from backend.App.Service.Dataset_Service import DatasetService

dataset_bp = Blueprint("dataset_bp", __name__)


@dataset_bp.route("/datasets", methods=["POST"])
def cadastra_dataset():
    data = request.get_json(silent=True) or {}
    url  = data.get("url")
    nome = data.get("nome")
    desc = data.get("descricao")

    response, status = DatasetService.cadastra(url, nome, desc)
    return jsonify(response), status


@dataset_bp.route("/datasets/<path:url>", methods=["GET"])
def consulta_dataset(url: str):
    response, status = DatasetService.consulta(url)
    return jsonify(response), status


@dataset_bp.route("/datasets", methods=["GET"])
def consulta_datasets():
    response, status = DatasetService.consulta_todos()
    return jsonify(response), status


@dataset_bp.route("/datasets/<path:url>", methods=["PATCH"])
def altera_dataset(url: str):
    data = request.get_json(silent=True) or {}
    nome = data.get("nome")
    desc = data.get("descricao")

    response, status = DatasetService.altera(url, nome, desc)
    return jsonify(response), status


@dataset_bp.route("/datasets/<path:url>", methods=["DELETE"])
def remove_dataset(url: str):
    response, status = DatasetService.remove(url)
    return jsonify(response), status


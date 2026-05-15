import json
import os
import subprocess

from flask import Blueprint, jsonify, request

amostra_bp = Blueprint("amostra_bp", __name__)


@amostra_bp.route("/usuario/coleta_amostra", methods=["POST"])
def coletar_amostra():
    data = request.get_json(silent=True) or {}

    n = str(data.get("n") or "")
    p = str(data.get("p") or "")
    f = str(data.get("f") or "")

    if n.strip() == "" or p.strip() == "" or f.strip() == "":
        return jsonify({"erro": "Parâmetros n, p e f são obrigatórios"}), 400

    try:
        caminho_codigo = os.path.join(os.path.dirname(__file__), "..", "..", "Scripts", "script_salvar.py")
        caminho_codigo = os.path.abspath(caminho_codigo)

        comando = ["python", caminho_codigo, "-n", n, "-p", p, "-f", f]
        resultado = subprocess.run(comando, capture_output=True, text=True)

        if resultado.returncode != 0:
            return jsonify({"erro": (resultado.stderr or "").strip()}), 500

        saida = json.loads((resultado.stdout or "").strip())
        return jsonify(saida), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


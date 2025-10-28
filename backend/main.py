import json
import os
import subprocess

from flask import request, jsonify

from App.Model.models import Usuario, Dataset, Modelo
from App.Service.Dispositivo_Service import DispositivoService
from App.Service.Usuario_Service import UsuarioService
from App.Service.Dataset_Service import DatasetService
from App.config import app, db


# qualquer coisa eu vou tentar mudar esse id para UUID, SE DER E PRECISAR
# routes para manipulação com usuário
@app.route("/login", methods=['POST'])
def logar_usuario():
    data = request.json

    email = data.get("email")
    senha = data.get("senha")

    response, status = UsuarioService.login(email, senha)
    return jsonify({"mensagem": response}), status


@app.route("/usuarios", methods=['POST'])
def cadastra_usuario():
    data = request.json

    email = data.get("email")
    senha = data.get("senha")

    response, status = UsuarioService.cadastra(email, senha)
    return jsonify({"mensagem": response}), status


@app.route("/usuarios/<id>", methods=['GET'])
def consulta_usuario(id: int):
    response, status = UsuarioService.consulta(id)
    return jsonify({"mensagem": response}), status


@app.route("/usuarios", methods=['GET'])
def consulta_usuarios():
    response, status = UsuarioService.consulta_todos()
    return jsonify({"mensagem": response}), status


@app.route("/usuarios/<id>", methods=["PATCH"])
def altera_usuario(id: int):
    nova_senha = request.json.get("nova_senha")

    response, status = UsuarioService.altera(id, nova_senha)
    return jsonify({"mensagem": response}), status


@app.route("/usuarios/<id>", methods=["DELETE"])
def remove_usuario(id: int):
    response, status = UsuarioService.remove(id)
    return jsonify({"mensagem": response}), status


# routes para manipulação de dispositivos
@app.route("/dispositivos", methods=["POST"])
def cadastra_dispositivo():
    data = request.json

    nome      = data.get("nome")
    descricao = data.get("descricao")
    codigo    = data.get("codigo")
    script    = data.get("script")

    resopnse, status = DispositivoService.cadastra(nome, descricao, codigo, script)
    return jsonify({"mensagem": resopnse}), status


@app.route("/dispositivos/<codigo>", methods=["PATCH"])
def altera_dispositivo(codigo: str):
    data = request.json

    nome      = data.get("nome")
    descricao = data.get("descricao")
    script    = data.get("script")

    response, status = DispositivoService.altera(codigo, nome, descricao, script)
    return jsonify({"mensagem": response}), status


@app.route("/dispositivos/<codigo>", methods=["DELETE"])
def remove_dispositivo(codigo: str):
    response, status = DispositivoService.remove(codigo)
    return jsonify({"mensagem": response}), status


@app.route("/dispositivos/<codigo>", methods=["GET"])
def consulta_dispositivo(codigo: str):
    response, status = DispositivoService.consulta(codigo)
    return jsonify({"mensagem": response}), status


@app.route("/dispositivos", methods=["GET"])
def consulta_dispositivos():
    response, status = DispositivoService.consulta_todos()
    return jsonify({"mensagem": response}), status


# routes para manipulação de datasets
# EM TESTAGEM
@app.route("/datasets", methods=["POST"])
def cadastra_dataset(url: str):
    data = request.json

    nome = data.get("nome")
    desc = data.get("descricao")

    response, status = DatasetService.cadastra(url, nome, desc)
    return jsonify({"mensagem": response}), status


@app.route("/datasets/<url>", methods=["GET"])
def consulta_dataset(url: str):
    response, status = DatasetService.consulta(url)
    return jsonify({"mensagem": response}), status


@app.route("/datasets", methods=["GET"])
def consulta_datasets():
    response, status = DatasetService.consulta_todos()
    return jsonify({"mensagem": response}), status


@app.route("/datasets/<url>", methods=["PATCH"])
def altera_dataset(url: str):
    data = request.json

    nome = data.get("nome")
    desc = data.get("descricao")

    response, status = DatasetService.altera(url, nome, desc)
    return jsonify({"mensagem": response}), status


@app.route("/datasets/<url>", methods=["DELETE"])
def remove_dataset(url: str):
    response, status = DatasetService.remove(url)
    return jsonify({"mensagem": response}), status


# routes para modelos
@app.route("/usuario/cadastra_modelo", methods=["POST"])
def cadastra_modelo():

        data = request.json

        email = data.get("email")
        if not email:
                return jsonify({"mensagem": "informe seu email"}), 400

        usuario = Usuario.query.filter(Usuario.email == email).first()
        if not usuario:
                return jsonify({"mensagem": "esse email não está cadastrado"}), 403

        url = data.get("url")
        if not url:
                return jsonify({"mensagem": "informe o url do modelo"}), 400
        
        nome = data.get("nome")
        desc = data.get("descricao")

        modelo = Modelo(
                id_usuario = usuario.id,
                url = url,
                nome = nome,
                descricao = desc
        )

        json_modelo = modelo.to_Json()

        try:
                db.session.add(modelo)
                db.session.commit()

        except Exception as e:
                db.session.rollback()
                return jsonify({"mensagem": "não foi possível cadastrar", "causa": str(e)}), 400
        
        return jsonify({"mensagem": "cadastrado", "modelo": json_modelo}), 200


@app.route("/usuario/consulta_modelo", methods=["GET"])
def consulta_modelo():

        data = request.json

        url = data.get("url")
        if not url:
                return jsonify({"mensagem": "informe a url do modelo"}), 400

        modelo = Modelo.query.filter(Modelo.url == url).first()
        if not modelo:
                return jsonify({"mensagem": "nenhum modelo encontrado com essa url"}), 403

        json_modelo = modelo.to_Json()

        return jsonify({"modelo encontrado": json_modelo}), 200


@app.route("/usuario/altera_modelo", methods=["PATCH"])
def altera_modelo():
        
        data = request.json

        url = data.get("url")
        if not url:
                return jsonify({"mensagem": "informe a url do modelo que deseja alterar"}), 400

        modelo = Modelo.query.filter(Modelo.url == url).first()
        if not modelo:
                return jsonify({"mensagem": "modelo não encontrado"}), 403

        nova_url = data.get("nova_url")
        novo_nome = data.get("nome")
        nova_desc = data.get("desc")
        
        if nova_url:
                modelo.url = nova_url

        if novo_nome:
                modelo.nome = novo_nome
        
        if nova_desc:
                modelo.descricao = nova_desc

        try:
                db.session.commit()

        except Exception as e:
                db.session.rollback()
                return jsonify({"mensagem": "não foi possível submeter as mudanças", "causa": str(e)}), 400
        
        return jsonify({"mensagem": "alterações salvas"}), 200


@app.route("/usuario/remove_modelo", methods=["DELETE"])
def remove_modelo():

        data = request.json
        
        url = data.get("url")
        if not url:
                return jsonify({"mensagem": "informe o url do modelo"}), 400

        modelo = Modelo.query.filter(Modelo.url == url).first()
        if not modelo:
                return jsonify({"mensagem": "nenhum modelo com essa url encontrado"}), 403
        
        try:
                db.session.delete(modelo)
                db.session.commit()

        except Exception as e:
                db.session.rollback()
                return jsonify({"mensagem": "não foi possível deletar seu modelo", "causa": str(e)}), 400


        return jsonify({"mensagem": "modelo deletado"}), 200

       
# route para pegar amostras e salvar elas
@app.route("/usuario/coleta_amostra", methods=['POST'])
def coletar_amostra():
        
        data = request.get_json()

        n = str(data.get('n'))
        p = data.get('p')
        f = data.get('f')

        if n.strip() == "" or p.strip() == "" or f.strip() == "":
                return jsonify({'erro': 'Parâmetros n, p e f são obrigatórios'}), 400

        try:
                # caso tenha que mudar o caminho ou o nome do código muda aqui que facilita
                caminho_codigo = os.path.join(os.path.dirname(__file__), 'Scripts', 'script_salvar.py')

                comando = ['python', caminho_codigo, '-n', n, '-p', p, '-f', f]

                resultado = subprocess.run(comando, capture_output=True, text=True)

                if resultado.returncode != 0:
                        return jsonify({'erro': resultado.stderr.strip()}), 500

                saida = json.loads(resultado.stdout.strip())
                return jsonify(saida), 200

        except Exception as e:
                return jsonify({'erro': str(e)}), 500



if __name__ == "__main__":
         
        with app.app_context():
                db.create_all()        
        
        app.run(debug=True)

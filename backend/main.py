import os
import subprocess
import json
from flask import request, jsonify
from App.config import app, db
from App.Model.models import Usuario, Dispositivo, Dataset, Modelo
from App.Service.Usuario_Service import UsuarioService

# fazer um atributo único como o id para encontrar melhor, por enquanto usarei id mesmo
# routes para manipulação com usuário
@app.route("/login", methods=['POST'])
def logar_usuario():

    data  = request.json
    email = data.get("email")
    senha = data.get("senha")

    response, status = UsuarioService.login(email, senha)
    return jsonify({"mensagem": response}), status


@app.route("/usuarios", methods=['POST'])
def cadastra_usuario():

    data  = request.json
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


# começar a mexer aqui
# routes para manipulação de dispositivos
@app.route("/usuario/cadastra_dispositivo", methods=["POST"])
def cadastra_dispositivo():

        data = request.json

        codigo_disp = data.get("codigo")
        if not codigo_disp:
                return jsonify({"mensagem": "informe o código para criação"}), 400

        nome_dispo = data.get("nome")
        desc_dispo = data.get("descrição")
        script_dispo = data.get("script")

        novo_dispositivo = Dispositivo(
                nome = nome_dispo,
                codigo = codigo_disp,
                descricao = desc_dispo,
                script = script_dispo
        )

        json_disp = novo_dispositivo.to_Json()

        try:
                db.session.add(novo_dispositivo)
                db.session.commit()

        except Exception as e:
                db.session.rollback() # desfaz o que tinha feito
                return jsonify({"mensagem": f"não deu pra cadastrar no banco de dados: {str(e)}"}), 400


        return jsonify({"mensagem": "tudo criado", "dispositivo": json_disp}), 201


@app.route("/usuario/altera_dispositivo", methods=["PATCH"])
def altera_dispositivo():
        
        data = request.json

        codigo_disp = data.get("codigo")        
        if not codigo_disp:
                return jsonify({"mensagem": "informe o código do dispositivo"}), 400
        
        dispositivo = Dispositivo.query.filter(Dispositivo.codigo == codigo_disp).first()
        if not dispositivo:
                return jsonify({"mensagem": "esse código não consta no banco de dados"}), 403

        novo_nome = data.get("nome")
        nova_desc = data.get("descrição")
        novo_script = data.get("script")

        if novo_nome:
                dispositivo.nome = novo_nome

        if nova_desc:
                dispositivo.descricao = nova_desc

        if novo_script:
                dispositivo.script_configuracao = novo_script

        try:
                db.session.commit()

        except Exception as e:
                db.session.rollback()
                return jsonify({"mensagem": f"deu um problema pra alterar no bd:: {str(e)}"}), 400

        return jsonify({"mensagem": "dados alterados"}), 200


@app.route("/usuario/remove_dispositivo", methods=["DELETE"])
def remove_dispositivo():

        data = request.json

        codigo = data.get("codigo")
        if not codigo:
                return jsonify({"mensagem": "nenhum código informado"}), 400

        disp = Dispositivo.query.filter(Dispositivo.codigo == codigo).first()           
        if not disp:
                return jsonify({"mensagem": "dispositivo não encontrado"}), 403

        try:
                db.session.delete(disp)
                db.session.commit()
        
        except Exception as e:
                db.session.rollback()
                return jsonify({"mensagem": "deu problema na hora de tirar do banco de dados", "causa": str(e)}), 400 

        return jsonify({"mensagem": "dispositivo removido"}), 200


@app.route("/usuario/consulta_dispositivo", methods=["GET"])
def consulta_dispositivo():

        data = request.json

        codigo = data.get("codigo")
        if not codigo:
                return jsonify({"mensagem": "nenhum código passado"}), 400

        disp = Dispositivo.query.filter(Dispositivo.codigo == codigo).first() 
        if not disp:
                return jsonify({"mensagem": "nenhum dispositivo encontrado"}), 403

        json_disp = disp.to_Json()

        return jsonify({"dispositivo": json_disp}), 200


# routes para manipulação de datasets
@app.route("/usuario/cadastra_dataset", methods=["POST"])
def cadastra_dataset():

        data = request.json

        url = data.get("url")
        if not url:
                return jsonify({"mensagem": "informe a url"}), 400
        
        nome = data.get("nome")
        desc = data.get("desc")

        dataset = Dataset(
                url = url, 
                nome = nome, 
                desc = desc
                )
        
        json_dataset = dataset.to_Json()

        try:
                db.session.add(dataset)
                db.session.commit()
        
        except Exception as e:
                db.session.rollback()
                return jsonify({"mensagem": "erro na hora de criar no banco de dados", "causa": str(e)}), 400

        return jsonify({"mensagem": "dataset cadastrado", "dataset": json_dataset}), 200


@app.route("/usuario/consulta_dataset", methods=["GET"])
def consulta_dataset():

        data = request.json

        url = data.get("url")
        if not url:
                return jsonify({"mensagem": "informe a url do dataset"}), 400

        dataset = Dataset.query.filter(Dataset.url == url).first()
        if not dataset:
                return jsonify({"mensagem": "nenhuma dataset com essa url encontrada"}), 403

        json_dataset = dataset.to_Json()
        return jsonify({"dataset encontrado": json_dataset}), 200


@app.route("/usuario/altera_dataset", methods=["PATCH"])
def altera_dataset():

        data = request.json

        url = data.get("url")
        if not url:
                return jsonify({"mensagem": "informe o url"}), 400

        dataset = Dataset.query.filter(Dataset.url == url).first()
        if not dataset:
                return jsonify({"mensagem": "nenhum dataset encontrado"}), 403 

        novo_nome = data.get("nome")
        nova_desc = data.get("desc")

        if novo_nome:
                dataset.nome = novo_nome
        
        if nova_desc:
                dataset.descricao = nova_desc

        try:
                db.session.commit()

        except Exception as e:
                db.session.rollback()
                return jsonify({"mensagem": "deu problema pra alterar", "causa": str(e)}), 400

        return jsonify({"mensagem": "dataset alterado"}), 200


@app.route("/usuario/remove_dataset", methods=["DELETE"])
def remove_dataset():

        data = request.json

        url = data.get("url")
        if not url:
                return jsonify({"mensagem": "informe o url"}), 400

        dataset = Dataset.query.filter(Dataset.url == url).first()
        if not dataset:
                return jsonify({"mensagem": "nenhum dataset encontrado"}), 403

        try:
                db.session.delete(dataset)
                db.session.commit()

        except Exception as e:
                db.session.rollback()
                return jsonify({"mensagem": "não foi possível tirar do banco de dados", "causa": str(e)}), 400

        return jsonify({"mensagem": "dataset deletado"}), 200


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

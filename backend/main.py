from flask import request, jsonify
from config import app, db
from tabelas import Usuario, Dispositivo, Dataset, Modelo

# routes para manipulação com usuário
@app.route("/login", methods=['GET'])
def logar_usuario():

        data = request.json

        email = data.get("email")
        senha = data.get("senha")

        # vendo se as informações bate
        usuario = Usuario.query.filter(Usuario.email == email, Usuario.senha == senha).first()

        if not usuario:
                return jsonify({"mensagem": "nunca vi tão gordo na vida :( "}), 400

        # o bem venceu
        return jsonify({"mensagem": "cidadão tá logado :)"}), 201



@app.route("/cadastra_usuario", methods=['POST'])
def cadastra_usuario():

        data = request.json

        email = data.get("email")
        senha = data.get("senha")

        if not email or not senha:
                return (
                        jsonify({"mensagem": "coloque as coisas primeiro "}), 400
                )
        

        novo_usuario = Usuario(email = email, senha = senha)
        # tentando colocar o usuário novo no banco de dados
        try:
                db.session.add(novo_usuario)
                db.session.commit()
                
        except Exception as e:
                return jsonify({"messagem": str(e)}), 400


        return jsonify({"mensagem": "Criado :)"}), 201



@app.route("/consulta_usuario", methods=['POST'])
def consulta_usuario():

        # pegando o email do usuario
        data = request.json
        email = data.get("email")

        if not email:
                return jsonify({"mensagem": "nenhum email passado"}), 400

        # hora da prova final
        usuario = Usuario.query.filter(Usuario.email == email).first()

        if not usuario:
                return jsonify({"mensagem": "ninguém tem nada parecido com isso ai"}), 400

        # como encontrou, eu passo ele pra json
        json_usuario = usuario.to_Json()
        return jsonify({"cidadão consultado": json_usuario}), 201



@app.route("/altera_usuario", methods=["POST"])
def altera_usuario():

        # pego o email antigo pra ver qual o usuário
        data = request.json

        email_antigo = data.get("email_antigo")
        nova_senha = data.get("nova_senha")
        
        if not email_antigo:
                return jsonify({"mensagem": "informe o email antigo"}), 400

        # pesquisando
        usuario = Usuario.query.filter(Usuario.email == email_antigo).first()
        
        if not usuario:
                return jsonify({"mensagem": "ninguém encontrado com esse email"}), 404

        if not nova_senha:
                return jsonify({"mensagem": "nenhuma senha passada"}), 401 

        # validando pra não repetir senha
        antiga_senha = usuario.senha
        
        if antiga_senha == nova_senha:
                return jsonify({"mensagem": "essa já era sua senha anterior"}), 400


        # agora que tá tudo bem
        usuario.senha = nova_senha
        db.session.commit()

        return jsonify({"mensagem": "senha alterada :)"}), 200



@app.route("/remove_usuario", methods=["POST"])
def remove_usuario():
        
        # pegando o email, já que ele é único
        data = request.json

        email = data.get("email")        
        
        if not email:
                return jsonify({"mensagem": "informe o email"}), 400
        
        # vendo se esse usuário existe
        usuario = Usuario.query.filter(Usuario.email == email).first()

        if not usuario:
                return jsonify({"mensagem": "usuário não encontrado"}), 404     
        
        # deletando do banco de dados
        try:
                db.session.delete(usuario)
                db.session.commit()
        
        except Exception as e:
                db.session.rollback()
                return jsonify({"mensagem": "deu ruim pra tirar do bd", "causa": str(e)}), 400
        
        return jsonify({"mensagem": "removido :)"}), 200


# routes para manipulação de dispositivos
@app.route("/usuario/cadastra_dispositivo", methods=["POST"])
def cadastra_dispositivo():

        # com pode acontecer de ter tudo repetido
        # eu deixei sem a verificação
        data = request.json

        nome_dispo = data.get("nome")
        codigo_disp = data.get("codigo")
        desc_dispo = data.get("descrição")
        script_dispo = data.get("script")
        

        # facilitando minha vida
        novo_dispositivo = Dispositivo(
                nome = nome_dispo,
                codigo = codigo_disp,
                descricao = desc_dispo,
                script = script_dispo
        )

        json_disp = novo_dispositivo.to_Json()

        # criação no banco de dados
        try:
                db.session.add(novo_dispositivo)
                db.session.commit()

        except Exception as e:
                db.session.rollback() # desfaz o que tinha feito
                return jsonify({"mensagem": f"não deu pra cadastrar no banco de dados: {str(e)}"}), 400


        return jsonify({"mensagem": "tudo criado", "dispositivo": json_disp}), 201



@app.route("/usuario/altera_dispositivo", methods=["POST"])
def altera_dispositivo():
        
        data = request.json

        # encontrando o codigo do dispositivo cadastrado (ele é único e não será mudado)
        codigo_disp = data.get("codigo")        

        if not codigo_disp:
                return jsonify({"mensagem": "informe o id do dispositivo"}), 400
        
        dispositivo = Dispositivo.query.filter(Dispositivo.codigo == codigo_disp).first()

        if not dispositivo:
                return jsonify({"mensagem": "esse código não consta no banco de dados"}), 403

        # agora que foi achado, podemos mudar suas coisas
        novo_nome = data.get("nome")
        nova_desc = data.get("descrição")
        novo_script = data.get("script")

        if novo_nome:
                dispositivo.nome = novo_nome

        if nova_desc:
                dispositivo.descricao = nova_desc

        if novo_script:
                dispositivo.script_configuracao = novo_script

        
        # salvando no banco de dados
        try:
                db.session.commit()

        except Exception as e:
                db.session.rollback()
                return jsonify({"mensagem": "deu um problema pra alterar no bd"}), 400                

        return jsonify({"mensagem": "dados alterados :D"}), 200

@app.route("/usuario/remove_dispositivo", methods=["POST"])
def remove_dispositivo():

        # verificando o código passado
        data = request.json
        codigo = data.get("codigo")

        if not codigo:
                return jsonify({"mensagem": "nenhum código informado"}), 400

        # procurando ele no banco de dados
        disp = Dispositivo.query.filter(Dispositivo.codigo == codigo).first()           

        if not disp:
                return jsonify({"mensagem": "dispositivo não encontrado"}), 403

        # comentário pra organização :D
        try:
                db.session.delete(disp)
                db.session.commit()
        
        except Exception as e:
                db.session.rollback()
                return jsonify({"mensagem": "deu problema na hora de tirar do banco de dados", "causa": str(e)}), 400 

        return jsonify({"mensagem": "dispositivo removido"}), 200


@app.route("/usuario/consulta_dispositivo", methods=["POST"])
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
        nome = data.get("nome")
        desc = data.get("desc")

        if not url:
                return jsonify({"mensagem": "informe a url"}), 400

        # mandando pro banco de dados
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
                return jsonify({"mensagem": "deu algum problema pra criar no banco de dados", "causa": str(e)}), 400

        return jsonify({"mensagem": "dataset cadastrado", "dataset": json_dataset}), 200


@app.route("/usuario/consulta_dataset", methods=["POST"])
def consulta_dataset():

        url = request.json.get("url")

        if not url:
                return jsonify({"mensagem": "informe a url do dataset"}), 400

        dataset = Dataset.query.filter(Dataset.url == url).first()

        if not dataset:
                return jsonify({"mensagem": "nenhuma dataset com essa url encontrada"}), 403

        json_dataset = dataset.to_Json()
        return jsonify({"dataset encontrado": json_dataset}), 200



@app.route("/usuario/altera_dataset", methods=["POST"])
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

        return jsonify({"mensagem": "alterado :)"}), 200


@app.route("/usuario/remove_dataset", methods=["POST"])
def remove_dataset():

        url = request.json.get("url")

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
        nome = data.get("nome")
        desc = data.get("descricao")

        if not url:
                return jsonify({"mensagem": "informe o url do modelo"}), 400
        
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


# então, daqui pra baixo eu não consegui testar pq meu postman simplesmente não quis abrir
# eu ainda vou testar ele quando ele voltar a abrir
# NÃO FAÇA NADA COM AS COISAS DAS FUNÇÕES DE BAIXO
# EU AINDA VOU TESTAR ISSO TUDO NO POSTMAN
@app.route("/usuario/consulta_modelo", methods=["POST"])
def consulta_modelo():

        url = request.json.get("url")
        if not url:
                return jsonify({"mensagem": "informe a url do modelo"}), 400


        modelo = Modelo.query.filter(Modelo.url == url).first()
        if not modelo:
                return jsonify({"mensagem": "nenhum modelo encontrado com essa url"}), 403

        
        json_modelo = modelo.to_Json()

        return jsonify({"modelo encontrado": json_modelo}), 200



@app.route("/usuario/altera_modelo", methods=["POST"])
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



@app.route("/usuario/remove_modelo", methods=["POST"])
def remove_modelo():

        url = request.json.get("url")

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

       

# aqui tá normal 
if __name__ == "__main__":
        
        # toda vez que rodar, cria as se precisar, se precisar 
        with app.app_context():
                db.create_all()        
        
        app.run(debug=True)























































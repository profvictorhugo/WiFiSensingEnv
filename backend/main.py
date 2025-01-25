from flask import request, jsonify
from config import app, db
from tabelas import Usuario


@app.route("/login", methods=['GET'])
def logar_usuario():
        email = request.json.get("email")
        senha = request.json.get("senha")

        # vendo se as informações bate
        cidadao = Usuario.query.filter(Usuario.email == email, Usuario.senha == senha).first()

        if not cidadao:
                return jsonify({"mensagem": "nunca vi tão gordo na vida :( )"}) 

        # o bem venceu
        return jsonify({"mensagem": "cidadão tá logado :)"})



@app.route("/cadastra_usuario", methods=['POST'])
def cadastra_usuario():
        email = request.json.get("email")
        senha = request.json.get("senha")

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



@app.route("/consulta_usuarios", methods=['POST'])
def consulta_usuarios():

        # pegando o email do usuario
        email = request.json.get("email")
        usuario = Usuario.query.filter(Usuario.email == email).first()

        # hora da prova final
        if not usuario:
                return jsonify({"mensagem": "ninguém tem nada parecido com isso ai"})

        # como encontrou, eu passo ele pra json
        json_usuario = usuario.to_Json()
        return jsonify({"cidadão consultado": json_usuario})




if __name__ == "__main__":
        
        # toda vez que rodar, cria as se precisar, se precisar 
        with app.app_context():
                db.create_all()        
        
        app.run(debug=True)























































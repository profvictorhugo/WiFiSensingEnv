from config import db

class Usuario(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(120), unique=True, nullable=False)
        senha = db.Column(db.String(16), nullable=False)


        def to_Json(self):
                return {
                        "id": self.id,
                        "email": self.email,
                        "senha": self.senha
                }



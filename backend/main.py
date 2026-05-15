from App.Configuration.config import app, db
from App.Routes.register_routes import register_routes


register_routes(app)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)


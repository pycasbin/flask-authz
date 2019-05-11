from flask import Flask
from casbin_middleware.middleware import CasbinMiddleware

app = Flask(__name__)
app.wsgi_app = CasbinMiddleware(app.wsgi_app)


@app.route("/")
def hello_world():
    return "Hello World!"


if __name__ == '__main__':
    app.run()

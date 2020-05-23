from flask import Flask
from manu import testRoute

app = Flask('__name__')
app.register_blueprint(testRoute, url_prefix='/manu')

if __name__ == '__main__':
    app.run(debug=True)
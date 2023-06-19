from flask import Flask, render_template, Blueprint

from functions.routes1 import routes1

app = Flask(__name__)

app.register_blueprint(routes1, url_prefix='/')


@app.route('/')
def home():
    return render_template('indexNoLog.html')

if __name__ == '__main__':
    app.run()
    context = ('cert.pem','key.pem')
    app.run(ssl_context=context, port=443, debug=True)

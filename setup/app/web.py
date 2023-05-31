from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main.html')

if __name__ == '__main__':
    context = ('cert.pem','key.pem')
    app.run(ssl_context=context, port=443, debug=True)

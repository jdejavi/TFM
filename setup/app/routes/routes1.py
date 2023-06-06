from flask import Flask, Blueprint

routes1 = Blueprint('routes1', __name__)


@routes1.route('/login')
def login():
    return '¡Ruta de login!'

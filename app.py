import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-change-me')
@app.route('/index')
def index():
    return render_template('index.html', show_menu=True)

@app.route('/owners', methods=['GET'])
def owners():
    donos = []
    return redirect(url_for('clientes_view'))

clientes = []
produtos = []
bebidas = []
pedidos = []

@app.route('/clientes', methods=['GET', 'POST'])
def clientes_view():
    return render_template('clientes.html', show_menu=True)

@app.route('/produtos', methods=['GET', 'POST'])
def produtos_view():
    return render_template('produtos.html', show_menu=True)

@app.route('/bebidas', methods=['GET', 'POST'])
def bebidas_view():
    return render_template('bebidas.html', show_menu=True)

@app.route('/pedidos', methods=['GET', 'POST'])
def pedidos_view():
    return render_template('pedidos.html', show_menu=True)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Aceita qualquer credencial enviada e redireciona para a página inicial
        login_val = request.form.get('login')
        password_val = request.form.get('password')
        flash('Login aceito.', 'success')
        return redirect(url_for('index'))
    return render_template('login.html', show_menu=False)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    return render_template('registro.html', show_menu=False)

# Verifica se o arquivo é o principal do projeto
if __name__ == '__main__':
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', '5600'))
    app.run(host=host, port=port, debug=True)

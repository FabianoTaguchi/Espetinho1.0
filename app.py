import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
# Necessário para uso de sessões (flash, etc.)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-change-me')

@app.route('/index')
def index():
    return render_template('index.html', show_menu=True)

@app.route('/owners', methods=['GET'])
def owners():
    donos = []
    # Substituído pelo cadastro de clientes em /clientes
    return redirect(url_for('clientes_view'))

clientes = []
produtos = []
bebidas = []
pedidos = []

@app.route('/clientes', methods=['GET', 'POST'])
def clientes_view():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        cpf = request.form.get('cpf', '').strip()
        email = request.form.get('email', '').strip()
        telefone = request.form.get('telefone', '').strip()
        if not nome:
            flash('Informe ao menos o nome do cliente.', 'warning')
            return redirect(url_for('clientes_view'))
        clientes.append({
            'id': len(clientes) + 1,
            'nome': nome,
            'cpf': cpf or None,
            'email': email or None,
            'telefone': telefone or None,
        })
        flash('Cliente cadastrado com sucesso.', 'success')
        return redirect(url_for('clientes_view'))
    return render_template('clientes.html', clientes=clientes, show_menu=True)

@app.route('/produtos', methods=['GET', 'POST'])
def produtos_view():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        preco_raw = request.form.get('preco', '0').strip()
        try:
            preco = float(preco_raw)
        except ValueError:
            preco = 0.0
        if not nome:
            flash('Informe o nome do espetinho.', 'warning')
            return redirect(url_for('produtos_view'))
        produtos.append({
            'id': len(produtos) + 1,
            'nome': nome,
            'preco': max(preco, 0.0),
        })
        flash('Espetinho cadastrado com sucesso.', 'success')
        return redirect(url_for('produtos_view'))
    return render_template('produtos.html', produtos=produtos, show_menu=True)

@app.route('/bebidas', methods=['GET', 'POST'])
def bebidas_view():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        tamanho = request.form.get('tamanho', '').strip() or None
        preco_raw = request.form.get('preco', '0').strip()
        try:
            preco = float(preco_raw)
        except ValueError:
            preco = 0.0
        if not nome:
            flash('Informe o nome da bebida.', 'warning')
            return redirect(url_for('bebidas_view'))
        bebidas.append({
            'id': len(bebidas) + 1,
            'nome': nome,
            'tamanho': tamanho,
            'preco': max(preco, 0.0),
        })
        flash('Bebida cadastrada com sucesso.', 'success')
        return redirect(url_for('bebidas_view'))
    return render_template('bebidas.html', bebidas=bebidas, show_menu=True)

@app.route('/pedidos', methods=['GET', 'POST'])
def pedidos_view():
    if request.method == 'POST':
        cliente_id_raw = request.form.get('cliente_id', '').strip()
        if not cliente_id_raw:
            flash('Selecione um cliente para o pedido.', 'warning')
            return redirect(url_for('pedidos_view'))
        try:
            cliente_id = int(cliente_id_raw)
        except ValueError:
            flash('Cliente inválido.', 'warning')
            return redirect(url_for('pedidos_view'))

        esp_ids = request.form.getlist('item_produto_id')
        esp_qtds = request.form.getlist('item_produto_qtd')
        beb_ids = request.form.getlist('item_bebida_id')
        beb_qtds = request.form.getlist('item_bebida_qtd')

        itens_espetinho = []
        for pid_raw, qtd_raw in zip(esp_ids, esp_qtds):
            if not pid_raw:
                continue
            try:
                pid = int(pid_raw)
                qtd = int(qtd_raw or '0')
            except ValueError:
                continue
            prod = next((p for p in produtos if p['id'] == pid), None)
            if prod and qtd > 0:
                itens_espetinho.append({
                    'id': pid, 'nome': prod['nome'], 'qtd': qtd, 'preco_unit': prod['preco'],
                    'total': prod['preco'] * qtd,
                })

        itens_bebida = []
        for bid_raw, qtd_raw in zip(beb_ids, beb_qtds):
            if not bid_raw:
                continue
            try:
                bid = int(bid_raw)
                qtd = int(qtd_raw or '0')
            except ValueError:
                continue
            beb = next((b for b in bebidas if b['id'] == bid), None)
            if beb and qtd > 0:
                itens_bebida.append({
                    'id': bid, 'nome': beb['nome'], 'tamanho': beb.get('tamanho'), 'qtd': qtd, 'preco_unit': beb['preco'],
                    'total': beb['preco'] * qtd,
                })

        if not itens_espetinho and not itens_bebida:
            flash('Adicione ao menos um espetinho ou uma bebida.', 'warning')
            return redirect(url_for('pedidos_view'))

        cliente = next((c for c in clientes if c['id'] == cliente_id), None)
        if not cliente:
            flash('Cliente não encontrado.', 'warning')
            return redirect(url_for('pedidos_view'))

        total = sum(i['total'] for i in itens_espetinho) + sum(i['total'] for i in itens_bebida)
        pedido = {
            'id': len(pedidos) + 1,
            'cliente_id': cliente_id,
            'cliente_nome': cliente['nome'],
            'espetinhos': itens_espetinho,
            'bebidas': itens_bebida,
            'total': total,
        }
        pedidos.append(pedido)
        flash('Pedido registrado com sucesso.', 'success')
        return redirect(url_for('pedidos_view'))

    return render_template('pedidos.html', clientes=clientes, produtos=produtos, bebidas=bebidas, pedidos=pedidos, show_menu=True)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login', '').strip()
        password = request.form.get('password', '')
        if not login or not password:
            flash('Informe usuário e senha.', 'warning')
            return redirect(url_for('login'))
        
        # Aceita qualquer combinação por enquanto
        flash('Login aceito.', 'success')
        return redirect(url_for('index'))
    return render_template('login.html', show_menu=False)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        login_val = request.form.get('login', '').strip()
        password_val = request.form.get('password', '')
        if not login_val or not password_val:
            flash('Informe login e senha.', 'warning')
            return redirect(url_for('registro'))
        # Sem persistência no estado original; apenas feedback
        flash('Conta criada (simulado). Faça login para continuar.', 'success')
        return redirect(url_for('login'))
    return render_template('registro.html', show_menu=False)

# (sem registro de usuário no estado anterior)

# Verifica se o arquivo é o principal do projeto
if __name__ == '__main__':
    # Runner da aplicação (configurável via env HOST/PORT)
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', '5600'))
    app.run(host=host, port=port, debug=True)

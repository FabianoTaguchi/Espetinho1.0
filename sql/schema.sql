-- Domínio de pedidos de espetinho
CREATE TABLE IF NOT EXISTS cliente (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT NOT NULL,
  cpf TEXT UNIQUE,
  email TEXT,
  telefone TEXT
);

CREATE TABLE IF NOT EXISTS produto (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT NOT NULL,
  preco REAL NOT NULL CHECK (preco >= 0)
);

CREATE TABLE IF NOT EXISTS bebida (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT NOT NULL,
  tamanho TEXT,
  preco REAL NOT NULL CHECK (preco >= 0)
);

CREATE TABLE IF NOT EXISTS pedido (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cliente_id INTEGER NOT NULL,
  criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (cliente_id) REFERENCES cliente(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS pedido_item (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pedido_id INTEGER NOT NULL,
  tipo TEXT NOT NULL CHECK (tipo IN ('espetinho','bebida')),
  referencia_id INTEGER NOT NULL,
  nome TEXT NOT NULL,
  tamanho TEXT,
  qtd INTEGER NOT NULL CHECK (qtd > 0),
  preco_unit REAL NOT NULL CHECK (preco_unit >= 0),
  total REAL NOT NULL CHECK (total >= 0),
  FOREIGN KEY (pedido_id) REFERENCES pedido(id) ON DELETE CASCADE
);

-- Usuários para autenticação
CREATE TABLE IF NOT EXISTS usuario (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  login TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL
);
/* Apaga tabelas antigas se elas existirem */
DROP TABLE IF EXISTS itens_pedido;
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS pagamentos;
DROP TABLE IF EXISTS produtos;
DROP TABLE IF EXISTS clientes;

/* Cria a tabela de clientes */
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    pais TEXT,
    data_cadastro DATE
);

/* Cria a tabela de produtos */
CREATE TABLE produtos (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    categoria TEXT,
    preco REAL
);

/* Cria a tabela de pedidos */
CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY,
    cliente_id INTEGER,
    data_pedido DATE,
    total REAL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

/* Cria a tabela de itens do pedido (tabela de junção) */
CREATE TABLE itens_pedido (
    pedido_id INTEGER,
    produto_id INTEGER,
    quantidade INTEGER,
    preco_unitario REAL,
    PRIMARY KEY (pedido_id, produto_id),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

/* Cria a tabela de pagamentos */
CREATE TABLE pagamentos (
    id INTEGER PRIMARY KEY,
    pedido_id INTEGER,
    data_pagamento DATE,
    valor REAL,
    metodo TEXT,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
);

/* --- Insere dados de exemplo --- */

INSERT INTO clientes (id, nome, pais, data_cadastro) VALUES
 (1,'Alice','EUA','2024-01-05'),
 (2,'Bruno','REINO UNIDO','2024-03-10'),
 (3,'Carla','COREIA','2024-06-22'),
 (4,'Daniel','BRASIL','2025-01-15');

INSERT INTO produtos (id, nome, categoria, preco) VALUES
 (1,'Notebook Pro','Eletrônicos',7500.00),
 (2,'Fone com Cancelamento de Ruído','Eletrônicos',1500.00),
 (3,'Mesa com Regulagem','Móveis',2250.00),
 (4,'Cadeira Ergonômica','Móveis',1250.00),
 (5,'Monitor 27"','Eletrônicos',1750.00);

INSERT INTO pedidos (id, cliente_id, data_pedido, total) VALUES
 (1,1,'2025-02-01',10750.00),
 (2,2,'2025-02-03',3500.00),
 (3,3,'2025-02-05',1750.00),
 (4,1,'2025-02-07',2250.00);

INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES
 (1,1,1,7500.00),
 (1,2,1,1500.00),
 (1,5,1,1750.00),
 (2,3,1,2250.00),
 (2,4,1,1250.00),
 (3,5,1,1750.00),
 (4,3,1,2250.00);

INSERT INTO pagamentos (id, pedido_id, data_pagamento, valor, metodo) VALUES
 (1,1,'2025-02-01',10750.00,'Cartão de Crédito'),
 (2,2,'2025-02-03',3500.00,'PayPal'),
 (3,3,'2025-02-05',1750.00,'Cartão de Crédito'),
 (4,4,'2025-02-07',2250.00,'Transferência Bancária');
-- 1. Product Table (Tabela de Produto)
CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    quantity BIGINT NOT NULL
);

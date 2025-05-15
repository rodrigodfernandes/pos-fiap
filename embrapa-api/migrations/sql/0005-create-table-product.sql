-- 1. Product Table (Tabela de Produto)
CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    wine_derivative_name wine_derivative_type not null,
    quantity BIGINT NOT NULL
);

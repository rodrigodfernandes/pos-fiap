-- 5. Wine Derivative Type Table (Tabela de Tipo de Vinhos e Derivados)
CREATE TABLE wine_derivative_type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

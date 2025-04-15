-- 7. Grape Type Table (Tabela de Tipo de Uva)
CREATE TABLE grape_type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);
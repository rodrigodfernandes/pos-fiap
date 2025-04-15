-- 2. Type Table (Tabela de Tipos)
CREATE TABLE kind (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

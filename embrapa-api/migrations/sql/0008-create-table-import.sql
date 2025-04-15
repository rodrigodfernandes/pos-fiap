-- 8. Import Table (Tabela de Importação)
CREATE TABLE import (
    id SERIAL PRIMARY KEY,
    grape_type_id INTEGER REFERENCES grape_type(id),
    country VARCHAR(100) NOT NULL,
    quantity_kg NUMERIC(15,2),
    value_usd NUMERIC(15,2)
);

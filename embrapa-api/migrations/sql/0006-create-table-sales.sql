-- 6. Sales Table (Tabela de Comercialização)
CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    wine_type_id INTEGER REFERENCES wine_derivative_type(id),
    quantity_liters NUMERIC(15,2) NOT NULL
);

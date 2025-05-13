-- 5. Sales Table (Tabela de Comercialização)
CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    wine_derivative_name wine_derivative_type not null,
    quantity_liters NUMERIC(15,2) NOT NULL
);

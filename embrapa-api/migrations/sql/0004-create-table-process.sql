-- 4. Processing Table (Tabela de Processamento)
CREATE TABLE process (
    id SERIAL PRIMARY KEY,
    color_name color not null,
    kind_name kind not null,
    cultivar VARCHAR(100) NOT NULL,
    quantity_kg BIGINT NOT NULL
);

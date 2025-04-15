-- 4. Processing Table (Tabela de Processamento)
CREATE TABLE process (
    id SERIAL PRIMARY KEY,
    color_id INTEGER REFERENCES color(id),
    kind_id INTEGER REFERENCES kind(id),
    cultivar VARCHAR(100) NOT NULL,
    quantity_kg BIGINT NOT NULL
);